# OdontoCA v1.9.2 â€” SDD 5.0, TDD 5.0 e Fluxograma Interativo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XnrsVU2u1Cq9igbRJHralBQrgtCYaksW)
[![Notebook](https://img.shields.io/badge/notebook-v1.9.2-2f81f7?logo=jupyter)](./OdontoCA_v1_9_2_FLUXOGRAMA_INTERATIVO_PAN_ZOOM.ipynb)
[![SDD](https://img.shields.io/badge/SDD-5.0-5b5bd6)](#sdd-50--tdd-50)
[![TDD](https://img.shields.io/badge/TDD-5.0-7a52c7)](#sdd-50--tdd-50)
[![Status](https://img.shields.io/badge/status-pesquisa%20%7C%20nÃ£o%20validado%20clinicamente-orange)](#limitaÃ§Ãµes-e-seguranÃ§a)

> Pipeline cientÃ­fico multimodal, reproduzÃ­vel e orientado por dados reais para modelagem de progressÃ£o de cÃ¡rie em nÃ­vel dentÃ¡rio, microbioma oral e visÃ£o computacional/radiogrÃ¡fica.

**Autor:** Marcelo Claro Laranjeira â€” Professor de Geografia e Pedagogo, CrateÃºs/CE, Brasil  
**ORCID:** [0000-0001-8996-2887](https://orcid.org/0000-0001-8996-2887)  
**GitHub:** [@MarceloClaro](https://github.com/MarceloClaro)  
**GeoMaker:** [bit.ly/geomaker](https://bit.ly/geomaker)

---

## Estado atual validado no Colab

A versÃ£o corrente do notebook Ã© a **v1.9.2**, em modo `SOMENTE_DADOS_REAIS=True`, com **SDD 5.0**, **TDD 5.0** e fluxograma interativo com pan, zoom, minimapa e navegaÃ§Ã£o por 16 camadas.

O arquivo salvo atualmente no Colab executou com sucesso o braÃ§o clÃ­nico-longitudinal atÃ© o modelo OOF clÃ­nico-espacial. Os mÃ³dulos de microbioma, adaptaÃ§Ã£o/curadoria visual, treinamento YOLO, runner TDD completo e exportaÃ§Ã£o final estÃ£o implementados, mas **ainda nÃ£o foram concluÃ­dos na execuÃ§Ã£o salva atualmente**. Portanto, este README separa explicitamente o que estÃ¡ **implementado** do que jÃ¡ foi **executado com dados reais**.

| Componente | Implementado | Executado na sessÃ£o salva | SituaÃ§Ã£o |
|---|:---:|:---:|---|
| SDD 5.0 / TDD 5.0 â€” especificaÃ§Ã£o | âœ… | âœ… | 46 requisitos e 58 testes carregados |
| `Table_S1.xlsx` â€” ingestÃ£o/contrato | âœ… | âœ… | aprovado |
| ReconstruÃ§Ã£o longitudinal por dente | âœ… | âœ… | contagens reproduzidas exatamente |
| Modelo clÃ­nico-espacial OOF | âœ… | âœ… | resultados reais disponÃ­veis |
| Qiita 14341 / microbioma | âœ… | â³ | nÃ£o concluÃ­do na sessÃ£o salva |
| Adaptadores universais de imagem | âœ… | â³ | nÃ£o concluÃ­dos na sessÃ£o salva |
| QC visual / deduplicaÃ§Ã£o / balanceamento | âœ… | â³ | nÃ£o concluÃ­dos na sessÃ£o salva |
| Treinamentos YOLO por domÃ­nio | âœ… | â³ | mÃ©tricas finais ainda nÃ£o promovidas |
| FDI / associaÃ§Ã£o lesÃ£o-dente | âœ… experimental | â³ | depende do braÃ§o visual/segmentaÃ§Ã£o |
| Runner TDD completo e acceptance gates | âœ… | â³ | depende dos mÃ³dulos downstream |
| Manifesto/ZIP final | âœ… | â³ | somente apÃ³s todos os gates |

---

## Resultado clÃ­nico real jÃ¡ reproduzido

O notebook reproduziu integralmente as contagens esperadas do braÃ§o clÃ­nico-longitudinal:

| Auditoria | Valor reproduzido |
|---|---:|
| Registros de metadados | 2.504 |
| CrianÃ§as | 89 |
| Registro composto `T5161` | 220 |
| Registros de dente individual | 2.284 |
| TransiÃ§Ãµes observadas | 1.388 |
| TransiÃ§Ãµes consecutivas `Î”timepoint=1` | 1.160 |
| `Hâ†’H` | 913 |
| `Hâ†’C` | 84 |
| `Câ†’C` | 163 |
| `Câ†’H` | 0 |
| Coorte de onset | 997 |

A execuÃ§Ã£o corrente do modelo clÃ­nico-espacial usa validaÃ§Ã£o aninhada agrupada por crianÃ§a e produziu:

| MÃ©trica | Resultado |
|---|---:|
| `n` | 997 |
| Eventos `Hâ†’C` | 84 |
| PrevalÃªncia | 0,084253 |
| PR-AUC | **0,182278** |
| ROC-AUC | **0,738825** |
| Brier | **0,078490** |
| Log Loss | **0,274674** |

Nos cinco folds externos registrados, a sobreposiÃ§Ã£o de pacientes entre treino e teste foi **zero**.

> Estes valores correspondem ao braÃ§o clÃ­nico da execuÃ§Ã£o atual da v1.9.2. Eles nÃ£o representam desempenho final multimodal nem validaÃ§Ã£o clÃ­nica externa.

---

## Arquitetura multimodal

O OdontoCA mantÃ©m domÃ­nios de evidÃªncia separados atÃ© que exista chave vÃ¡lida para integraÃ§Ã£o.

```text
DADOS REAIS
â”‚
â”œâ”€â”€ ClÃ­nica longitudinal â€” Table_S1 / Single-tooth ECC
â”‚   â””â”€â”€ crianÃ§a Ã— dente Ã— tempo â†’ Hâ†’C
â”‚
â”œâ”€â”€ Microbioma oral â€” Qiita Study 14341 / BIOM
â”‚   â””â”€â”€ SampleID â†’ ASV â†’ CLR â†’ modelo nested
â”‚
â”œâ”€â”€ Fotografia intraoral â€” Zenodo 14827784
â”‚   â””â”€â”€ detecÃ§Ã£o visual de cÃ¡rie
â”‚
â”œâ”€â”€ PanorÃ¢mica pediÃ¡trica â€” Kaggle
â”‚   â”œâ”€â”€ Children Caries Detection Dataset
â”‚   â””â”€â”€ Children's Dental Panoramic Radiographs
â”‚
â”œâ”€â”€ Anatomia dentÃ¡ria â€” Dental Anatomy YOLOv8
â”‚
â””â”€â”€ SegmentaÃ§Ã£o/FDI â€” SegmentAnyTooth (opcional/licenciado)
```

A fusÃ£o em nÃ­vel de paciente Ã© bloqueada quando nÃ£o sÃ£o simultaneamente satisfeitas as chaves:

```text
mesma coorte
+ patient_id
+ visit_id
+ tooth_fdi
```

---

## SDD 5.0 + TDD 5.0

O projeto utiliza **Specification-Driven Development** e **Test-Driven Development** como contratos metodolÃ³gicos executÃ¡veis.

### SDD 5.0

- **46 requisitos obrigatÃ³rios**;
- governanÃ§a e proveniÃªncia;
- contrato de schema externo;
- modelagem clÃ­nica sem variÃ¡veis futuras;
- nested preprocessing do microbioma;
- ausÃªncia de leakage por paciente;
- tratamento visual anti-leakage;
- polÃ­tica de split conservadora;
- isolamento do conjunto de teste;
- interoperabilidade FHIR;
- reprodutibilidade e seguranÃ§a cientÃ­fica.

### TDD 5.0

**58 testes especificados antes das implementaÃ§Ãµes:**

| NÃ­vel | Testes |
|---|---:|
| UNIT | 20 |
| INTEGRATION | 15 |
| ACCEPTANCE | 23 |
| **Total** | **58** |

O runner final produz `PASS`, `SKIP` ou `FAIL`. Um `FAIL` obrigatÃ³rio bloqueia a promoÃ§Ã£o dos resultados.

---

## BraÃ§o clÃ­nico-longitudinal

O pipeline:

1. lÃª `Table_S1.xlsx` preservando os nomes externos publicados;
2. valida as 24 colunas obrigatÃ³rias;
3. remove o registro composto `T5161`;
4. organiza observaÃ§Ãµes por crianÃ§a, dente e tempo;
5. reconstrÃ³i `t â†’ t+1`;
6. mantÃ©m somente `Î”timepoint = 1`;
7. restringe a coorte de onset aos dentes hÃ­gidos em `t`;
8. define `0 = Hâ†’H` e `1 = Hâ†’C`;
9. utiliza validaÃ§Ã£o externa e interna agrupada por crianÃ§a;
10. usa PR-AUC como mÃ©trica primÃ¡ria de discriminaÃ§Ã£o para o evento raro.

A representaÃ§Ã£o clÃ­nica inclui contexto local de vizinhanÃ§a dentÃ¡ria e features topolÃ³gicas experimentais de antÃ­meros. O notebook tambÃ©m possui um Ã­ndice experimental de vulnerabilidade salivar; essas features devem ser interpretadas como modelagem de pesquisa e nÃ£o como regra clÃ­nica validada.

---

## Microbioma oral

O mÃ³dulo microbiolÃ³gico foi projetado para o **Qiita Study 14341**, com associaÃ§Ã£o determinÃ­stica `SampleID â†” BIOM`.

O preprocessing fica dentro do pipeline aninhado:

```text
ASV
 â†“
filtro no treino
 â†“
pseudocontagem
 â†“
CLR
 â†“
StandardScaler
 â†“
PCA
 â†“
tuning interno
 â†“
prediÃ§Ã£o OOF
```

O notebook compara trÃªs modelos no mesmo subconjunto pareado:

- clÃ­nico;
- microbioma;
- combinado clÃ­nico + microbioma.

O valor incremental Ã© estimado com bootstrap por crianÃ§a, preservando a estrutura de cluster.

---

## VisÃ£o computacional e radiogrÃ¡fica

### Adaptadores universais de anotaÃ§Ã£o

A v1.9.x nÃ£o pressupÃµe uma estrutura Ãºnica de dataset. O inventÃ¡rio tenta reconhecer e converter, de forma auditÃ¡vel:

1. YAML YOLO oficial;
2. TXT YOLO pareado globalmente por `stem`;
3. LabelMe JSON;
4. COCO JSON;
5. Pascal VOC XML;
6. CSV com bounding boxes;
7. mÃ¡scaras binÃ¡rias/semÃ¢nticas â†’ bounding boxes YOLO.

Imagens sem ground truth sÃ£o separadas como `inference_only` e nÃ£o sÃ£o convertidas silenciosamente em exemplos negativos.

### PolÃ­tica de split

```text
split oficial disponÃ­vel?
â”œâ”€â”€ sim â†’ preservar
â””â”€â”€ nÃ£o
    â”œâ”€â”€ patient_id confiÃ¡vel â†’ Group split por paciente
    â””â”€â”€ sem patient_id â†’ train + val para desenvolvimento
                         NÃƒO fabricar test independente
```

### Controle de qualidade

O notebook calcula por imagem:

- largura e altura;
- intensidade mÃ©dia;
- contraste;
- variÃ¢ncia do Laplaciano;
- flag de blur;
- baixo contraste;
- subexposiÃ§Ã£o;
- superexposiÃ§Ã£o.

Por padrÃ£o, imagens difÃ­ceis nÃ£o sÃ£o excluÃ­das automaticamente apenas para aumentar a mÃ©trica.

### Curadoria anti-leakage

- SHA-256 por imagem;
- deduplicaÃ§Ã£o exata entre splits com prioridade `test > val > train`;
- near-duplicates auditados por dHash + BK-tree;
- distribuiÃ§Ã£o de classes e Ã¡reas das caixas;
- reamostragem limitada somente no `train`;
- `val` e `test` permanecem inalterados.

### Tuning e treinamento

A seleÃ§Ã£o de configuraÃ§Ã£o utiliza **somente validaÃ§Ã£o**:

```text
configuraÃ§Ã£o-base â”€â”
                   â”œâ”€ treino curto â†’ comparar em val â†’ selecionar
configuraÃ§Ã£o tratadaâ”˜                              â†“
                                            treino final
                                                 â†“
                                          best.pt + SHA-256
                                                 â†“
                                  test legÃ­timo, quando disponÃ­vel
```

O projeto mantÃ©m fotografia intraoral, panorÃ¢mica pediÃ¡trica e anatomia dentÃ¡ria como domÃ­nios separados.

---

## AssociaÃ§Ã£o lesÃ£o â†” dente e odontograma

A v1.9.2 possui associaÃ§Ã£o geomÃ©trica experimental baseada em **Intersection over Lesion (IoL)**:

```text
IoL = Ã¡rea(interseÃ§Ã£o entre lesÃ£o e dente) / Ã¡rea da lesÃ£o
```

A associaÃ§Ã£o Ã© usada somente quando existe detecÃ§Ã£o/segmentaÃ§Ã£o dentÃ¡ria compatÃ­vel. Casos ambÃ­guos devem seguir para revisÃ£o profissional; detecÃ§Ã£o de cÃ¡rie nÃ£o Ã© automaticamente convertida em nÃºmero FDI sem suporte geomÃ©trico apropriado.

---

## Fluxograma interativo

O notebook incorpora um fluxograma Mermaid/HTML/JavaScript com **16 camadas** e controles locais:

- zoom `+` / `âˆ’`;
- roda do mouse centrada no cursor;
- pan por mouse, toque ou caneta;
- botÃ£o `100%`;
- enquadramento automÃ¡tico;
- centralizaÃ§Ã£o;
- setas de navegaÃ§Ã£o;
- menu **Ir para** por camada;
- minimapa sincronizado;
- atalhos `+`, `-`, `0`, `1` e setas.

A interface do fluxograma Ã© independente da execuÃ§Ã£o cientÃ­fica: falha de renderizaÃ§Ã£o nÃ£o deve interromper o pipeline.

---

## Datasets registrados

| Fonte | Modalidade | Papel no projeto |
|---|---|---|
| HuangShiLab / Single-tooth ECC | longitudinal por dente | trajetÃ³ria clÃ­nica e target `Hâ†’C` |
| Qiita 14341 | microbioma 16S | valor incremental microbiolÃ³gico |
| Zenodo `10.5281/zenodo.14827784` | fotografia intraoral | detecÃ§Ã£o de cÃ¡rie |
| Children Caries Detection Dataset | panorÃ¢mica pediÃ¡trica | detecÃ§Ã£o de cÃ¡rie infantil |
| Children's Dental Panoramic Radiographs | panorÃ¢mica pediÃ¡trica | cÃ¡rie/doenÃ§as dentÃ¡rias |
| Dental Anatomy Dataset â€” YOLOv8 | imagem odontolÃ³gica | anatomia/localizaÃ§Ã£o |
| SegmentAnyTooth | fotografia intraoral | segmentaÃ§Ã£o e FDI opcional |
| MD-OPG | panorÃ¢mica pediÃ¡trica | candidato futuro para segmentaÃ§Ã£o por superfÃ­cie |

Os datasets visuais nÃ£o sÃ£o automaticamente pareados com a coorte longitudinal. AusÃªncia de chave comum implica bloqueio de fusÃ£o em nÃ­vel de paciente.

---

## Como executar

### Google Colab â€” recomendado

Abra diretamente:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XnrsVU2u1Cq9igbRJHralBQrgtCYaksW)

Depois:

1. selecione um runtime com GPU para o braÃ§o visual;
2. reinicie a sessÃ£o se estiver reutilizando um runtime antigo;
3. execute as cÃ©lulas em ordem;
4. nÃ£o avance quando um gate obrigatÃ³rio falhar;
5. para resultados cientÃ­ficos, utilize somente saÃ­das geradas por dados reais.

### Jupyter / VS Code

```bash
git clone https://github.com/MarceloClaro/OdontoCA.git
cd OdontoCA

python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
jupyter lab
```

DependÃªncias principais declaradas em `requirements.txt`: NumPy, pandas, SciPy, scikit-learn, openpyxl, requests, matplotlib, Pillow, PyYAML, biom-format e Ultralytics.

---

## Estrutura atual do repositÃ³rio

```text
OdontoCA/
â”œâ”€â”€ LICENSE
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â””â”€â”€ OdontoCA_v1_9_2_FLUXOGRAMA_INTERATIVO_PAN_ZOOM.ipynb
```

---

## Artefatos previstos pelo pipeline

Quando a execuÃ§Ã£o integral for aprovada, o notebook prevÃª exportar, entre outros:

- requisitos SDD;
- especificaÃ§Ãµes e resultados TDD;
- matriz de rastreabilidade SDD â†’ TDD;
- auditorias clÃ­nicas e microbiolÃ³gicas;
- inventÃ¡rios e QC visual;
- registros de falhas de parsing;
- prediÃ§Ãµes OOF;
- mÃ©tricas dos modelos;
- resultados de tuning;
- pesos `best.pt` com SHA-256;
- manifesto de reprodutibilidade;
- relatÃ³rio de validaÃ§Ã£o;
- `RiskAssessment` FHIR experimental;
- pacote ZIP final de resultados.

---

## Regra de promoÃ§Ã£o cientÃ­fica

```text
DADO REAL
   â†“
INTEGRIDADE E PROVENIÃŠNCIA
   â†“
SEM LEAKAGE
   â†“
VALIDAÃ‡ÃƒO / OOF
   â†“
TDD + ACCEPTANCE GATES
   â†“
APPROVED â€” PIPELINE DE PESQUISA
```

`APPROVED` significa que os requisitos do pipeline de pesquisa foram satisfeitos. **NÃ£o significa validaÃ§Ã£o clÃ­nica, autorizaÃ§Ã£o regulatÃ³ria ou desempenho comprovado para uso assistencial.**

---

## LimitaÃ§Ãµes e seguranÃ§a

- finalidade exclusivamente cientÃ­fica e educacional;
- nÃ£o Ã© dispositivo mÃ©dico;
- nÃ£o substitui avaliaÃ§Ã£o odontolÃ³gica;
- nenhuma fusÃ£o cross-cohort Ã© permitida sem chaves comuns vÃ¡lidas;
- patient-disjoint visual sÃ³ pode ser declarado quando existe identificaÃ§Ã£o confiÃ¡vel de paciente;
- resultados visuais e microbiolÃ³gicos devem ser considerados pendentes atÃ© execuÃ§Ã£o e aprovaÃ§Ã£o dos respectivos gates;
- o recurso FHIR permanece `preliminary`;
- mÃ©tricas sintÃ©ticas nÃ£o podem ser promovidas a resultados cientÃ­ficos.

---

## LicenÃ§a

Consulte o arquivo [`LICENSE`](./LICENSE) deste repositÃ³rio para os termos de uso do cÃ³digo. Datasets, artigos e pesos de terceiros permanecem sujeitos Ã s licenÃ§as de suas respectivas fontes.
