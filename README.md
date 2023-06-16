# Avaliação Sprints 9 e 10 - Projeto Final - Programa de Bolsas Compass UOL / AWS e Univesp

Avaliação das sprints 9 e 10 do programa de bolsas Compass UOL para formação em machine learning para AWS.

---
*Capa*

# Introdução

Projeto de desenvolvimento de um chatbot dedicado a auxiliar no reforço da alfabetização de crianças, especialmente diante dos desafios enfrentados pelo setor da educação no Brasil durante a pandemia. Este projeto foi impulsionado pela necessidade de fornecer uma solução que possa ajudar as crianças a superarem as dificuldades de aprendizado.

A pandemia da COVID-19 trouxe consigo uma série de desafios sem precedentes, afetando significativamente o setor da educação. Com o fechamento das escolas e a transição para o ensino remoto, muitas crianças enfrentaram interrupções em seu processo de alfabetização, uma fase fundamental para o desenvolvimento de habilidades de leitura e escrita. A falta de interação presencial com professores e colegas, além da limitada disponibilidade de recursos educacionais, levou a lacunas no aprendizado e diminuição do engajamento das crianças.


# Objetivo 

- Com base no contexto apresentado, o projeto visa utilizar o chatbot, como uma ferramenta de inteligência artificial, de forma a auxiliar a preencher essa lacuna e proporcionar um ambiente de aprendizagem virtual interativo e eficaz e promover acesso à educação e combater as consequências negativas da pandemia, garantindo que as crianças tenham a oportunidade de desenvolver habilidades de alfabetização.


# Funcionamento 

# Organização e fluxo de trabalho 

# Arquitetura 

<div align="center">
  <img src="./assets/arquitetura-atual.jpg">
  <sub>
    <p>Arquitetura do projeto</p><br>
  </sub>
</div>


## Serviços utilizados

- [Amazon Lex](https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html)
    * [Amazon Recokgnition](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html) 
    * [Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html)
    * [Amazon Translate](https://docs.aws.amazon.com/translate/latest/dg/what-is.html)
- [Twilio](https://www.twilio.com/pt-br/docs)
    * [Whatsapp](https://business.whatsapp.com/developers/developer-hub)

# Instalação

## Etapas

- Definição do tema e construção da Arquietura base do projeto;
- Criar chatbot utilizando Amazon Lex;
- Integrar com seguintes serviços da AWS: Rekognition, Translate e Transcribe 
- Criar uma conta no [Twilio](https://www.twilio.com/)
- Integrar com Whatsapp

## Integrando o Amazon Lex com o Whatsapp via Twilio

- Twilio Console -> My account -> Copiar SID e Token
- Amazon Lex Console -> Bot versions -> Deployment -> Channel Integrations -> Add channel -> Platform - Twilio SMS -> Inserir Account SID e Authentication token -> Create -> Copiar url de endpoint gerado
- Twilio Console -> Messaging -> Settings -> Whatsapp sandbox settings -> Colar endpoint copiado em WHEN A MESSAGE COMES IN

# Dificuldades 

# Referências 

[Kondado](https://kondado.com.br/blog/wiki/2020/11/03/adicionando-o-s3-como-destino-na-plataforma-da-kondado/)

# Desenvolvedores 

[<img src="https://avatars.githubusercontent.com/u/97908745?v=4" width=115><br><sub>Ana Vitória</sub>](https://github.com/anaVitoriaLouro) | [<img src="https://avatars.githubusercontent.com/u/81330043?v=4" width=115><br><sub>Bernardo Lima</sub>](https://github.com/belima93) | [<img src="https://avatars.githubusercontent.com/u/87142990?v=4" width=115><br><sub>Luciene Godoy</sub>](https://github.com/LucieneGodoy) | [<img src="https://avatars.githubusercontent.com/u/72028902?v=4" width=115><br><sub>Luiz Sassi</sub>](https://github.com/luizrsassi) | [<img src="https://avatars.githubusercontent.com/u/88354075?v=4" width=115><br><sub>Kelly Silva</sub>](https://github.com/KellyPLSilva) | [<img src="https://avatars.githubusercontent.com/u/117780664?v=4" width=115><br><sub>Viviane Alves</sub>](https://github.com/Vivianes86)|
| :---: | :---: | :---: | :---: | :---: | :---: | 








