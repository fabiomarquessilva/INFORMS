
import streamlit as st
import csv
import os

try:
    from twilio.rest import Client
except ModuleNotFoundError:
    st.error("A biblioteca 'twilio' não está instalada. Por favor, instale-a executando 'pip install twilio'.")
    st.stop()

# Configuração inicial do aplicativo
st.set_page_config(page_title="Pesquisa sobre Farmacologia", layout="wide")

# Arquivo para armazenar as respostas
CSV_FILE = "student_survey_responses.csv"

# Função para salvar as respostas em CSV
def save_to_csv(data):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Adiciona cabeçalho apenas se o arquivo estiver vazio
            writer.writerow(["Nome", "Endereço", "Telefone", "E-mail", "Curso e Período", 
                             "Expectativas", "Tópicos Importantes", "Preferência de Aula", 
                             "Maiores Desafios", "Comentários Adicionais"])
        writer.writerow(data)

# Função para enviar mensagem via WhatsApp
def send_whatsapp_message(data):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "AC8156497a26e9e7c97da3c60a27561298")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "8ea6fedcc4c80d6aff9d5345f0e774d1")
    from_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+17752598306")
    to_whatsapp_number = "whatsapp:+5584994420139"

    try:
        client = Client(account_sid, auth_token)
        message_body = f"""        Nova resposta recebida:
        
        Nome: {data[0]}
        Endereço: {data[1]}
        Telefone: {data[2]}
        E-mail: {data[3]}
        Curso e Período: {data[4]}
        
        Expectativas: {data[5]}
        Tópicos Importantes: {data[6]}
        Preferência de Aula: {data[7]}
        Maiores Desafios: {data[8]}
        Comentários Adicionais: {data[9]}
        """

        message = client.messages.create(
            from_=from_whatsapp_number,
            body=message_body,
            to=to_whatsapp_number
        )
        st.success("Os dados foram enviados com sucesso via WhatsApp!")
    except Exception as e:
        st.error(f"Erro ao enviar a mensagem: {e}")

# Cabeçalho da página
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Pesquisa sobre a Disciplina de Farmacologia</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FF5722;'>Ajude-nos a entender suas expectativas!</h3>", unsafe_allow_html=True)

# Formulário de informações pessoais
with st.form("survey_form"):
    st.header("Informações Pessoais")
    name = st.text_input("Nome Completo")
    address = st.text_input("Endereço")
    phone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    course_period = st.text_input("Curso e Período")

    st.header("Expectativas sobre Farmacologia")
    expectations = st.text_area("O que você espera aprender em Farmacologia?")
    important_topics = st.text_area("Quais tópicos específicos você considera mais importantes?")
    preferred_approach = st.selectbox("Como prefere que as aulas sejam ministradas?", 
                                      ["Teoria", "Prática", "Estudos de Caso", "Outros"])
    challenges = st.text_area("Qual o maior desafio que você espera enfrentar na disciplina?")
    additional_comments = st.text_area("Comentários adicionais")

    submitted = st.form_submit_button("Enviar")
    if submitted:
        if not name or not email:
            st.error("Por favor, preencha os campos obrigatórios: Nome e E-mail.")
        else:
            # Salvando dados no CSV
            response_data = [name, address, phone, email, course_period, 
                             expectations, important_topics, preferred_approach, 
                             challenges, additional_comments]
            save_to_csv(response_data)
            
            # Enviando mensagem via WhatsApp
            send_whatsapp_message(response_data)
