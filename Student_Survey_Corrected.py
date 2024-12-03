
import streamlit as st
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Função para enviar e-mail com as respostas
def send_email(data):
    sender_email = "seu-email@gmail.com"
    sender_password = "sua-senha"
    receiver_email = "ffabioms3@gmail.com"
    
    subject = "Nova Resposta: Pesquisa de Farmacologia"
    body = f"""    Nome: {data[0]}
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

    # Configuração do e-mail
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Enviando o e-mail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            st.success("Os dados foram enviados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar o e-mail: {e}")

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
            
            # Enviando e-mail
            send_email(response_data)
