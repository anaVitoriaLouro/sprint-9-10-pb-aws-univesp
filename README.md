## Avaliação Sprints 9 e 10 - Projeto Final - Programa de Bolsas Compass UOL / AWS e Univesp

<div align="center">
  <h1 style="font-size: 32px;"><b>CompassBot</b></h1>
</div>


## Tema e Motivação

A solução proposta neste trabalho tem como intuito fomentar a acessibilidade a textos, áudios e imagens para atender necessidades de pessoas com distintas dificuldades na leitura e escrita.

Além de garantir a inclusão, buscaremos facilitar o acesso à informação para indivíduos que enfrentam limitações decorrentes de deficiência auditiva e visual, analfabetismo ou dislexia.

***

## Introdução

Muitas pessoas possuem limitações significativas devido a dificuldades na leitura e escrita, deficiência auditiva ou visual, analfabetismo e dislexia que dificultam o acesso à informação. Para auxiliar com essas limitações, foi desenvolvida esta aplicação prática que utiliza recursos e serviços da AWS para tornar os conteúdos mais acessíveis.

Esta solução oferece funcionalidades como: transcrição de áudio, síntese de voz, reconhecimento de imagens e um chatbot de atendimento para guiar o usuário. Ao utilizar serviços como o Amazon Lex Amazon, Transcribe, Polly e Rekognition, permitimos que pessoas com deficiências ou dificuldades específicas possam acessar informações relevantes por meio de diferentes modalidades.

O ChatBot de atendimento oferece suporte e esclarecimentos adicionais sobre o conteúdo acessível, interagindo com os usuários por meio de texto. Com a transcrição de áudio, tornamos os conteúdos audíveis em textos, permitindo que pessoas com deficiência auditiva tenham acesso à informação através da leitura. A síntese de voz, por sua vez, possibilita que textos sejam transformados em áudios, beneficiando pessoas com dificuldades na leitura ou com deficiência visual. Já o reconhecimento de imagens descreve as imagens em texto, permitindo que pessoas com deficiência visual entendam o conteúdo das mesmas.

***

## Objetivo

Desenvolver uma aplicação prática que promova a acessibilidade de textos, áudios e imagens, atendendo às necessidades de pessoas com dificuldades na leitura e escrita, deficiência auditiva ou visual, analfabetismo ou dislexia. Utilizaremos recursos e serviços da AWS, como o Amazon Transcribe, Amazon Polly, Amazon Rekognition e Amazon Lex, para implementar funcionalidades que tornem os conteúdos acessíveis por meio de diferentes modalidades.

***

## Ferramentas e Tecnologias utilizadas

* [Amazon Transcribe](https://aws.amazon.com/pt/transcribe/): para transcrever áudios em texto.
* [Amazon Polly](https://aws.amazon.com/pt/polly/): para sintetizar textos em áudios.
* [Amazon Rekognition](https://aws.amazon.com/pt/rekognition/): para descrever imagens.
* [Amazon Lex](https://aws.amazon.com/pt/lex/): para interação com os usuários.
* [Amazon S3](https://aws.amazon.com/pt/s3/): para armazenamento temporário de arquivos de mídia
* [Telegram](https://web.telegram.org/): plataforma escolhida para hospedar a aplicação

## Arquitetura do projeto

![Esboço](/assets/estrutura.PNG)
<div align="center">
  <sub>Escboço da arquitetura do projeto</sub>
</div>

***

## Funcionamento

A solução pode ser usada da seguinte maneira:

Com o Bot hospedado no Telegram, o usuário pode a qualquer momento iniciar uma conversa, verificar os serviços oferecidos pela solução e escolher qual deseja naquele momento.

Por exemplo, quando o usuário envia uma mensagem de áudio, existe um backend preparado para acionar o serviço do **Amazon Transcribe**, que por sua vez irá transcrever essa mensagem de áudio e devolver para o usuário uma mensagem de texto com todo o conteúdo daquele áudio.

No caso oposto, o usuário poderá enviar uma mensagem de texto que passara para o serviço do **Amazon Polly**, que realizará a síntese de voz a partir daquele texto, retornando ao usuário uma mensagem de áudio.

No terceiro caso, este usuário poderá tirar foto de uma placa de aviso ou uma escrita que contenha texto impresso ou escrito a mão. Essa imagemn será direcionada ao **Amazon Rekoignition** que fará a extração deste texto e caso não esteja em português, fará a tradução e enviará para o **Amazon Polly**, que usará esse texto para gerar áudio, e retornará ao usuário uma mensagem de voz.

***

## Requisitos

Para executar este projeto, é necessário que possua uma conta AWS.

[Clique aqui](https://aws.amazon.com/pt/console/) para criar sua conta AWS.

## Instalação e Implantação

Para implementar na sua conta, siga estes passos:

Clone este repostório

```bash
  git clone -b grupo-2 https://github.com/Compass-pb-aws-2023-Univesp/sprint-9-10-pb-aws-univesp.git

```

Certifique-se de ter as credenciais da sua conta AWS configuradas na sua máquina com a AWS CLI.

Siga [estes passos](https://docs.aws.amazon.com/pt_br/powershell/latest/userguide/pstools-appendix-sign-up.html) para obter suas credenciais de conta.

Configure o ambiente com sua Access Key e Secret Access Key:

```bash
  $ aws configure
  AWS Access Key ID [None]: accesskey
  AWS Secret Access Key [None]: secretkey
  Default region name [None]: us-west-2
  Default output format [None]:
```

Instale o framework serverless

```bash
  npm install -g serverless
```

Navegue até a pasta `src`

Inicie o deploy:

```bash
  serverless deploy
```

## Organização Geral do Código Fonte

Estrutura geral da organização do projeto

```a
.
├── src/
│   └── lambda_functions/
│       ├── modules
│       ├── services
│       ├── telegram_tools
│       └── utils
└── assets
```

## Dificuldades e Impedimentos superados

* Uso do Amazon LexV2 com Backend
* Criaçã ode uma função de gerenciamento para lidar com os eventos vindos do Telegram e repassá-los ao ChatBot

## Referências

Durante o desenvolvimento deste projeto, consultamos as seguintes referências:

- Documentação oficial da AWS: https://docs.aws.amazon.com/
- Documentação do Amazon Transcribe: https://docs.aws.amazon.com/transcribe/index.html
- Documentação do Amazon Polly: https://docs.aws.amazon.com/polly/index.html
- Documentação do Amazon Rekognition: https://docs.aws.amazon.com/rekognition/index.html
- Documentação do Amazon Lex: https://docs.aws.amazon.com/lex/index.html

## Desenvolvedores
[<img src="https://avatars.githubusercontent.com/u/25699466?v=4" width=115><br><sub>Bruno Perillo</sub>](https://github.com/brunoperillo) | [<img src="https://avatars.githubusercontent.com/u/78061851?v=4" width=115><br><sub>Carlos Camilo</sub>](https://github.com/crobertocamilo) | [<img src="https://avatars.githubusercontent.com/u/96358027?v=4" width=115><br><sub>Diego Lopes</sub>](https://github.com/Diegox0301) | [<img src="https://avatars.githubusercontent.com/u/124359272?v=4" width=115><br><sub>Irati Maffra</sub>](https://github.com/IratiMaffra) | [<img src="https://avatars.githubusercontent.com/u/73674662?v=4" width=115><br><sub>Marcos Nativo</sub>](https://github.com/onativo) | [<img src="https://avatars.githubusercontent.com/u/94749597?v=4" width=115><br><sub>O'Dhara Maggi</sub>](https://github.com/odharamaggi)|
| :---: | :---: | :---: | :---: | :---: | :---: |
