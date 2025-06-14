import streamlit as st
import json
import os
import datetime


# Nome do arquivo JSON
ARQUIVO_DADOS = "pacientes.json"

# Funções para manipulação do arquivo JSON
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def cadastrar_paciente():
    st.title("📋 Cadastrar Novo Paciente")
    
    # Carregar dados existentes
    dados = carregar_dados()
    
    # Formulário de cadastro
    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo*", placeholder="Digite o nome completo")
            cpf = st.text_input("CPF*", placeholder="000.000.000-00")
            telefone = st.text_input("Telefone*", placeholder="(00) 00000-0000")
            email = st.text_input("Email", placeholder="exemplo@email.com")
        
        with col2:
            data_nascimento = st.date_input("Data de Nascimento*", 
                                          min_value=datetime.date(1900, 1, 1),
                                          max_value=datetime.date.today())
            sexo = st.selectbox("Sexo*", ["", "Masculino", "Feminino", "Outro"])
            endereco = st.text_area("Endereço", placeholder="Rua, número, bairro, cidade")
            observacoes = st.text_area("Observações", placeholder="Informações adicionais")
        
        # Botão de submissão
        submitted = st.form_submit_button("💾 Cadastrar Paciente", use_container_width=True)
        
        if submitted:
            # Validações
            if not nome or not cpf or not telefone or not sexo:
                st.error("⚠️ Por favor, preencha todos os campos obrigatórios (*)!")
                return
            
            # Verificar se CPF já existe
            if cpf in dados:
                st.error("⚠️ CPF já cadastrado no sistema!")
                return
            
            # Criar novo paciente
            novo_paciente = {
                "nome": nome,
                "cpf": cpf,
                "telefone": telefone,
                "email": email,
                "data_nascimento": data_nascimento.strftime("%d/%m/%Y"),
                "sexo": sexo,
                "endereco": endereco,
                "observacoes": observacoes,
                "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            # Adicionar aos dados
            dados[cpf] = novo_paciente
            
            # Salvar no arquivo
            salvar_dados(dados)
            
            st.success("✅ Paciente cadastrado com sucesso!")
            st.balloons()
            
            # Mostrar dados cadastrados
            st.subheader("📄 Dados Cadastrados:")
            st.json(novo_paciente)


def listar_pacientes():
    st.title("📋 Lista de Pacientes")
    
    dados = carregar_dados()
    
    if not dados:
        st.warning("⚠️ Nenhum paciente cadastrado.")
        return
    
    st.info(f"📊 Total de pacientes cadastrados: {len(dados)}")
    
    # Converter dados para lista de dicionários
    pacientes = []
    for cpf, paciente in dados.items():
        # Adicionar CPF aos dados do paciente para exibição
        paciente_completo = paciente.copy()
        paciente_completo['CPF'] = cpf
        pacientes.append(paciente_completo)
    
    # Exibir tabela com todos os pacientes
    if pacientes:
        # Reorganizar colunas para melhor visualização
        colunas_ordem = ['CPF', 'nome', 'telefone', 'email', 'data_nascimento', 'sexo']
        
        # Criar DataFrame para melhor formatação
        import pandas as pd
        df = pd.DataFrame(pacientes)
        
        # Reordenar colunas se existirem
        colunas_existentes = [col for col in colunas_ordem if col in df.columns]
        outras_colunas = [col for col in df.columns if col not in colunas_ordem]
        df = df[colunas_existentes + outras_colunas]
        
        # Renomear colunas para exibição
        df = df.rename(columns={
            'nome': 'Nome',
            'telefone': 'Telefone', 
            'email': 'Email',
            'data_nascimento': 'Data Nascimento',
            'sexo': 'Sexo',
            'endereco': 'Endereço',
            'observacoes': 'Observações',
            'data_cadastro': 'Data Cadastro'
        })
        
        st.dataframe(df, use_container_width=True)
        
        # Seção de ações
        st.subheader("🔧 Ações")
        
        # Selectbox para escolher paciente
        opcoes_pacientes = {f"{paciente['nome']} - {cpf}": cpf for cpf, paciente in dados.items()}
        paciente_selecionado = st.selectbox(
            "Selecione um paciente para ver detalhes ou excluir:",
            [""] + list(opcoes_pacientes.keys())
        )
        
        if paciente_selecionado:
            cpf_selecionado = opcoes_pacientes[paciente_selecionado]
            paciente_dados = dados[cpf_selecionado]
            
            # Mostrar detalhes do paciente selecionado
            with st.expander("👤 Detalhes do Paciente", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Nome:** {paciente_dados['nome']}")
                    st.write(f"**CPF:** {cpf_selecionado}")
                    st.write(f"**Telefone:** {paciente_dados['telefone']}")
                    st.write(f"**Email:** {paciente_dados.get('email', 'Não informado')}")
                
                with col2:
                    st.write(f"**Data Nascimento:** {paciente_dados['data_nascimento']}")
                    st.write(f"**Sexo:** {paciente_dados['sexo']}")
                    st.write(f"**Data Cadastro:** {paciente_dados.get('data_cadastro', 'Não informado')}")
                
                if paciente_dados.get('endereco'):
                    st.write(f"**Endereço:** {paciente_dados['endereco']}")
                
                if paciente_dados.get('observacoes'):
                    st.write(f"**Observações:** {paciente_dados['observacoes']}")

        

def editar_paciente():
    None  

def excluir_paciente():
    None

# Menu lateral
st.sidebar.title("Menu")
opcao = st.sidebar.radio(
    "Selecione uma opção:",
    ("Cadastrar Paciente","Listar Pacientes", 
     "Editar Paciente", "Excluir Paciente")
)

# Navegação entre páginas
if opcao == "Cadastrar Paciente":
    cadastrar_paciente()
elif opcao == "Listar Pacientes":
    listar_pacientes()
elif opcao == "Editar Paciente":
    editar_paciente()
elif opcao == "Excluir Paciente":
    excluir_paciente()

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por Lucas Castro")
st.sidebar.markdown(f"Total de pacientes: ")
