# Automation Challenge

Projeto de automação de testes desenvolvido para o **desafio de API e Web/Mobile Testing**.
O objetivo é validar endpoints REST e fluxos funcionais (web/mobile) utilizando **Python**, **Pytest** e ferramentas auxiliares como **Requests**, **Selenium**, **Appium** e **Allure Reports**.

---

## Objetivos do Projeto

* Criar uma **suíte automatizada** de testes de API, web e mobile.
* Garantir a **validação de autenticação** das rotas fornecidas.
* Implementar **boas práticas de estruturação, versionamento e relatórios** de testes.

---

## Tecnologias Utilizadas

- Python 3.9.6
- Pytest
- Requests (testes de API)
- Selenium WebDriver (Web)
- Appium (Mobile)
- Allure Report
- RapidFuzz (comparação de strings)
- Page Object Model (POM)

---

## Como executar o projeto

### Clonar o repositório

```bash
git clone git@github.com:evog-jpg/automation-challenge.git
cd automation-challenge
```

### Criar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar os testes utilizando os markers adequados

#### por exemplo, execução de testes web:
```bash
pytest -m web
```
##### o pytest.ini está configurado para colocar os resultados no allure.

### Gerar relatório Allure (opcional):

```bash
allure serve allure-results
```

---

## Autor

**Eduardo Gerab**
[GitHub: evog-jpg](https://github.com/evog-jpg)

---
