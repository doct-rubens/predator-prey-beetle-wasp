# predator-prey-beetles-wasps

O sistema aqui descrito consiste em uma estruturação de dados e implementação de um modelo de simulação presa-predador, com o intuito de avaliar os resultados da interação entre vespas (espécie) e mariposas (espécie) no contexto de ccontrole de pragas em plantações de cana-de-açúcar na região sudeste do Brasil.

A descrição a seguir contém 
  1. Estrutura de dados
  2. Fluxo de informação
  3. Implementação (informação sobre cada subdiretório e arquivo do projeto)

1.. ESTRUTURA DE DADOS
----------------------
O sistema de simulação possui três classes implementadas seguindo uma estrutura orientada a objetos: as criaturas, o mundo e o universo. As relações entre essas classes são descritas de acordo com o diagrama de classes presente no arquivo de image "system-class-diagram.png". A função específica de cada uma dessas classes é descrita nas subseções abaixo.

> 1.1. Criatura
> -------------
> A classe __Criatura__ é abstrata. As criaturas do sistema biológico descrito não são representadas por instâncias dessa classe, mas sim de suas subclasses --- __Vespa__ e __Mariposa__. A classe-mãe possui as implementações de operações básicas de criaturas como nascimento, inicialização e morte, enquanto que as subclasses são usadas essencialmente pra diferenciar esses dois tipos de criaturas, bem como mudanças nas rotinas dos métodos implementados na classe-mãe.

> Os tipos de dados armazenados nesse nível são:
  1. gênero (macho ou fêmea)
  2. fertilidade (verdadeiro ou falso)
  3. tempo de vida (inteiro positivo, para o caso de morte por causas naturais --- excluindo predação e morte por causas aleatórias)
  4. idade (inteiro positivo)
  5. vivo (verdadeiro ou falso)
  6. geração (inteiro positivo)
  7. filhos (inteiro positivo)

> Adicionalmente, uma lista estática contendo referências para as instâncias de mariposas que estão na fase de lagarta é salva e atualizada pelo sistema.

> 1.2. Universo
> -------------
> A classe __Universo__ contém as informações intrínsecas ao funcionamento do sistema biológico. Em termos simples, uma instância dessa classe "segura" todas as informações e probabilidades da simulação. Ela é referenciada apenas por objetos da classe __Mundo__, responsável por de fato executar as simulações.

> Os tipos de dados armazenados em instâncias dessa classe são, para cada uma das criaturas:
  1. razão entre machos e fêmeas (real entre 0 e 1)
  2. média de tempo de vida (real)
  3. variância do tempo de vida (real)
  4. idade inicial mínima (inteiro)
  5. idade inicial máxima (inteiro)
  6. razão de fertilidade (real entre 0 e 1)
  7. média de filhos (real)
  8. variância de filhos (real)
  9. idade mínima de adulto (inteiro)
  10. idade máxima de ovo (inteiro)
  11. chance de morte por fatores aleatórios (real entre 0 e 1)

> Relativo aos dados independentes do tipo de criatura, tem-se:
  1. tipos de dados a serem salvos (lista)

> 1.3. Mundo
> ----------
> Uma única instância da classe mundo é responsável por executar e re-executar uma simulação quantas vezes forem necessárias. Seu principal método é o chamado *executar_mundo(params)*, que toma como parâmetros as quantidades iniciais de vespas e mariposas e o número de iterações (dias) da simulação. O retorno desse método é um *data frame* contendo, para cada instante da simulação (dia) e para cada tipo de criatura (vespas e mariposas), os seguintes dados (de tipo inteiro), descritos por um dos atributos de instâncias da classe __Universo__:
  1. vivas
  2. mortas
  3. machos
  4. fêmeas
  5. mortas aleatoriamente
  6. mortas por velhice 
  7. mães
  8. adultos
  9. recém-nascidos
  10. mortos por predação
  11. lagartas

> Os atributos da classe __Mundo__ são todos essenciais para a execução da simulação. Eles são listados a seguir:
  1. universo (instância de __Universo__)
  2. número inicial de vespas (inteiro)
  3. número inicial de mariposas (inteiro)
  4. criaturas (listas de instâncias de __Mariposa__ e __Vespa__)
  5. filhos (listas de instâncias de __Mariposa__ e __Vespa__)
  6. dados das iterações (*data frame* com dados a serem retornados)

> 1.4. Controle de Simulação
> --------------------------
> Uma instância da classe __Controle__ funciona como uma interface entre as execuções de simulações com dadas condições iniciais e o armazenamento dos dados gerados por essas simulações. Como parte desses resultados, essa classe também acomoda os métodos responsáveis por calcular o custo e o custo de Bayes associados a uma simulação. Para o custo simples, os dados são salvos no formato de um *data frame* com as seguintes colunas:
  1. número inicial de vespas (inteiro)
  2. número inicial de mariposas (inteiro)
  3. número de iterações (dias)
  4. número de simulações (inteiro --- o resultado é calculado a partir da média instante a instante das simulações com mesmas condições iniciais)
  5. custo (real)

> Para o custo de bayes, os dados são também armazenados em um *data frame* cujas colunas são listadas abaixo:
  1. número inicial de vespas (inteiro)
  2. número de mariposas na amostra (inteiro)
  3. área de amostragem (real positivo)
  4. custo de bayes (real)

> Os atributos da classe __Controle__ são dados como:
  1. mundo (instância de __Mundo__)
  2. custo de vespa (real)
  3. custo de mariposa (real)
  4. _plotter_ (instância de __Plotter__, classe auxiliar responsável pela geração de imagens e vídeos com resultados das simulações)
  5. Fator de densidade (real)

2.. FLUXO DE INFORMAÇÃO
-----------------------
As duas operações finais efetuadas pelo sistema são
  1. A geração, execução e documentação da simulação de um mundo em um número limitado de passos;  
  2. O cálculo do custo simples e custo de bayes associado a um intervalo de tempo e um mundo.
  
Para a execução de uma simulação, dois tipos de dados de entrada são necessários: as probabilidades e constantes de funcionamento do universo (armazenadas em uma instância da classe __Universo__) e o número de passos de iteração da simulação. Com esses dois dados, uma ou mais simulações podem ser executadas e documentadas (cf. figura "fluxo-informação.png").

Para efetuar o cálculo dos custos de uma simulação, são necessários como entradas as constantes de custo das criaturas (vespas e lagartas), bem como os dados da simulação, dois quais é extraída a quantidade de lagartas em função do tempo, essencial para esse cálculo.

3.. IMPLEMENTAÇÃO
----------------
O sistema é organizado em subdiretórios dedicados, cada um comportando a implementação de uma funcionalidade, série de classes ou dados específicos. Aqui temos:
  **1. _funcs_:** Funções auxiliares usadas ao longo do sistema
  > 1.1. _bayes.py_: Implementação do custo de bayes;
  >
  > 1.2. _init_default.py_: Inicialização padrão e instanciação de um objeto de cada uma das classes __Mundo__, __Universo__, __Controle__ e __Plotter__.

  **2. _data_:** Dados coletados externamente e armazenados em formato _.csv_.
  
  **3. _media_:** Funções dedicadas à geração de gráficos e vídeos de evolução de gráficos a partir dos dados de simulação.
  
  **4. _simul_:** Implementação das classes e métodos dedicados à execução da simulação e cálculo dos custos.
  > 4.1. _control.py_: Implementação da classe __Controle__.
  >
  > 4.2. _creatures.py_: Implementação das classes __Criatura__, __Vespa__ e __Mariposa__.
  >
  > 4.3. _universe.py_: Implementação da classe __Universo__.
  >
  > 4.4. _world.py_: Implementação da classe __Mundo__.
  
  **5. _tests_:** Scripts de teste do sistema.
