# OdontoCA v1.9.2 — SDD 5.0, TDD 5.0 e Fluxograma Interativo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XnrsVU2u1Cq9igbRJHralBQrgtCYaksW)
[![Notebook](https://img.shields.io/badge/notebook-v1.9.2-2f81f7?logo=jupyter)](./OdontoCA_v1_9_2_FLUXOGRAMA_INTERATIVO_PAN_ZOOM.ipynb)
[![SDD](https://img.shields.io/badge/SDD-5.0-5b5bd6)](#sdd-50--tdd-50)
[![TDD](https://img.shields.io/badge/TDD-5.0-7a52c7)](#sdd-50--tdd-50)
[![Status](https://img.shields.io/badge/status-pesquisa%20%7C%20não%20validado%20clinicamente-orange)](#limitações-e-segurança)

> Pipeline científico multimodal, reproduzível e orientado por dados reais para modelagem de progressão de cárie em nível dentário, microbioma oral e visão computacional/radiográfica.

**Autor:** Marcelo Claro Laranjeira — Professor de Geografia e Pedagogo, Crateús/CE, Brasil  
**ORCID:** [0000-0001-8996-2887](https://orcid.org/0000-0001-8996-2887)  
**GitHub:** [@MarceloClaro](https://github.com/MarceloClaro)  
**GeoMaker:** [bit.ly/geomaker](https://bit.ly/geomaker)

---

## Estado atual validado no Colab

A versão corrente do notebook é a **v1.9.2**, em modo `SOMENTE_DADOS_REAIS=True`, com **SDD 5.0**, **TDD 5.0** e fluxograma interativo com pan, zoom, minimapa e navegação por 16 camadas.

O arquivo salvo atualmente no Colab executou com sucesso o braço clínico-longitudinal até o modelo OOF clínico-espacial. Os módulos de microbioma, adaptação/curadoria visual, treinamento YOLO, runner TDD completo e exportação final estão implementados, mas **ainda não foram concluídos na execução salva atualmente**. Portanto, este README separa explicitamente o que está **implementado** do que já foi **executado com dados reais**.

| Componente | Implementado | Executado na sessão salva | Situação |
|---|:---:|:---:|---|
| SDD 5.0 / TDD 5.0 — especificação | ✅ | ✅ | 46 requisitos e 58 testes carregados |
| `Table_S1.xlsx` — ingestão/contrato | ✅ | ✅ | aprovado |
| Reconstrução longitudinal por dente | ✅ | ✅ | contagens reproduzidas exatamente |
| Modelo clínico-espacial OOF | ✅ | ✅ | resultados reais disponíveis |
| Qiita 14341 / microbioma | ✅ | ⏳ | não concluído na sessão salva |
| Adaptadores universais de imagem | ✅ | ⏳ | não concluídos na sessão salva |
| QC visual / deduplicação / balanceamento | ✅ | ⏳ | não concluídos na sessão salva |
| Treinamentos YOLO por domínio | ✅ | ⏳ | métricas finais ainda não promovidas |
| FDI / associação lesão-dente | ✅ experimental | ⏳ | depende do braço visual/segmentação |
| Runner TDD completo e acceptance gates | ✅ | ⏳ | depende dos módulos downstream |
| Manifesto/ZIP final | ✅ | ⏳ | somente após todos os gates |

---

## Resultado clínico real já reproduzido

O notebook reproduziu integralmente as contagens esperadas do braço clínico-longitudinal:

| Auditoria | Valor reproduzido |
|---|---:|
| Registros de metadados | 2.504 |
| Crianças | 89 |
| Registro composto `T5161` | 220 |
| Registros de dente individual | 2.284 |
| Transições observadas | 1.388 |
| Transições consecutivas `Δtimepoint=1` | 1.160 |
| `H→H` | 913 |
| `H→C` | 84 |
| `C→C` | 163 |
| `C→H` | 0 |
| Coorte de onset | 997 |

A execução corrente do modelo clínico-espacial usa validação aninhada agrupada por criança e produziu:

| Métrica | Resultado |
|---|---:|
| `n` | 997 |
| Eventos `H→C` | 84 |
| Prevalência | 0,084253 |
| PR-AUC | **0,182278** |
| ROC-AUC | **0,738825** |
| Brier | **0,078490** |
| Log Loss | **0,274674** |

Nos cinco folds externos registrados, a sobreposição de pacientes entre treino e teste foi **zero**.

> Estes valores correspondem ao braço clínico da execução atual da v1.9.2. Eles não representam desempenho final multimodal nem validação clínica externa.

---

## Arquitetura multimodal

O OdontoCA mantém domínios de evidência separados até que exista chave válida para integração.

```text
DADOS REAIS
│
├── Clínica longitudinal — Table_S1 / Single-tooth ECC
│   └── criança × dente × tempo → H→C
│
├── Microbioma oral — Qiita Study 14341 / BIOM
│   └── SampleID → ASV → CLR → modelo nested
│
├── Fotografia intraoral — Zenodo 14827784
│   └── detecção visual de cárie
│
├── Panorâmica pediátrica — Kaggle
│   ├── Children Caries Detection Dataset
│   └── Children's Dental Panoramic Radiographs
│
├── Anatomia dentária — Dental Anatomy YOLOv8
│
└── Segmentação/FDI — SegmentAnyTooth (opcional/licenciado)
```

A fusão em nível de paciente é bloqueada quando não são simultaneamente satisfeitas as chaves:

```text
mesma coorte
+ patient_id
+ visit_id
+ tooth_fdi
```

---

## SDD 5.0 + TDD 5.0

O projeto utiliza **Specification-Driven Development** e **Test-Driven Development** como contratos metodológicos executáveis.

### SDD 5.0

- **46 requisitos obrigatórios**;
- governança e proveniência;
- contrato de schema externo;
- modelagem clínica sem variáveis futuras;
- nested preprocessing do microbioma;
- ausência de leakage por paciente;
- tratamento visual anti-leakage;
- política de split conservadora;
- isolamento do conjunto de teste;
- interoperabilidade FHIR;
- reprodutibilidade e segurança científica.

### TDD 5.0

**58 testes especificados antes das implementações:**

| Nível | Testes |
|---|---:|
| UNIT | 20 |
| INTEGRATION | 15 |
| ACCEPTANCE | 23 |
| **Total** | **58** |

O runner final produz `PASS`, `SKIP` ou `FAIL`. Um `FAIL` obrigatório bloqueia a promoção dos resultados.

---

## Braço clínico-longitudinal

O pipeline:

1. lê `Table_S1.xlsx` preservando os nomes externos publicados;
2. valida as 24 colunas obrigatórias;
3. remove o registro composto `T5161`;
4. organiza observações por criança, dente e tempo;
5. reconstrói `t → t+1`;
6. mantém somente `Δtimepoint = 1`;
7. restringe a coorte de onset aos dentes hígidos em `t`;
8. define `0 = H→H` e `1 = H→C`;
9. utiliza validação externa e interna agrupada por criança;
10. usa PR-AUC como métrica primária de discriminação para o evento raro.

A representação clínica inclui contexto local de vizinhança dentária e features topológicas experimentais de antímeros. O notebook também possui um índice experimental de vulnerabilidade salivar; essas features devem ser interpretadas como modelagem de pesquisa e não como regra clínica validada.

---

## Microbioma oral

O módulo microbiológico foi projetado para o **Qiita Study 14341**, com associação determinística `SampleID ↔ BIOM`.

O preprocessing fica dentro do pipeline aninhado:

```text
ASV
 ↓
filtro no treino
 ↓
pseudocontagem
 ↓
CLR
 ↓
StandardScaler
 ↓
PCA
 ↓
tuning interno
 ↓
predição OOF
```

O notebook compara três modelos no mesmo subconjunto pareado:

- clínico;
- microbioma;
- combinado clínico + microbioma.

O valor incremental é estimado com bootstrap por criança, preservando a estrutura de cluster.

---

## Visão computacional e radiográfica

### Adaptadores universais de anotação

A v1.9.x não pressupõe uma estrutura única de dataset. O inventário tenta reconhecer e converter, de forma auditável:

1. YAML YOLO oficial;
2. TXT YOLO pareado globalmente por `stem`;
3. LabelMe JSON;
4. COCO JSON;
5. Pascal VOC XML;
6. CSV com bounding boxes;
7. máscaras binárias/semânticas → bounding boxes YOLO.

Imagens sem ground truth são separadas como `inference_only` e não são convertidas silenciosamente em exemplos negativos.

### Política de split

```text
split oficial disponível?
├── sim → preservar
└── não
    ├── patient_id confiável → Group split por paciente
    └── sem patient_id → train + val para desenvolvimento
                         NÃO fabricar test independente
```

### Controle de qualidade

O notebook calcula por imagem:

- largura e altura;
- intensidade média;
- contraste;
- variância do Laplaciano;
- flag de blur;
- baixo contraste;
- subexposição;
- superexposição.

Por padrão, imagens difíceis não são excluídas automaticamente apenas para aumentar a métrica.

### Curadoria anti-leakage

- SHA-256 por imagem;
- deduplicação exata entre splits com prioridade `test > val > train`;
- near-duplicates auditados por dHash + BK-tree;
- distribuição de classes e áreas das caixas;
- reamostragem limitada somente no `train`;
- `val` e `test` permanecem inalterados.

### Tuning e treinamento

A seleção de configuração utiliza **somente validação**:

```text
configuração-base ─┐
                   ├─ treino curto → comparar em val → selecionar
configuração tratada┘                              ↓
                                            treino final
                                                 ↓
                                          best.pt + SHA-256
                                                 ↓
                                  test legítimo, quando disponível
```

O projeto mantém fotografia intraoral, panorâmica pediátrica e anatomia dentária como domínios separados.

---

## Associação lesão ↔ dente e odontograma

A v1.9.2 possui associação geométrica experimental baseada em **Intersection over Lesion (IoL)**:

```text
IoL = área(interseção entre lesão e dente) / área da lesão
```

A associação é usada somente quando existe detecção/segmentação dentária compatível. Casos ambíguos devem seguir para revisão profissional; detecção de cárie não é automaticamente convertida em número FDI sem suporte geométrico apropriado.

---

## Fluxograma interativo

O notebook incorpora um fluxograma Mermaid/HTML/JavaScript com **16 camadas** e controles locais:

- zoom `+` / `−`;
- roda do mouse centrada no cursor;
- pan por mouse, toque ou caneta;
- botão `100%`;
- enquadramento automático;
- centralização;
- setas de navegação;
- menu **Ir para** por camada;
- minimapa sincronizado;
- atalhos `+`, `-`, `0`, `1` e setas.

A interface do fluxograma é independente da execução científica: falha de renderização não deve interromper o pipeline.

---

## Datasets registrados

| Fonte | Modalidade | Papel no projeto |
|---|---|---|
| HuangShiLab / Single-tooth ECC | longitudinal por dente | trajetória clínica e target `H→C` |
| Qiita 14341 | microbioma 16S | valor incremental microbiológico |
| Zenodo `10.5281/zenodo.14827784` | fotografia intraoral | detecção de cárie |
| Children Caries Detection Dataset | panorâmica pediátrica | detecção de cárie infantil |
| Children's Dental Panoramic Radiographs | panorâmica pediátrica | cárie/doenças dentárias |
| Dental Anatomy Dataset — YOLOv8 | imagem odontológica | anatomia/localização |
| SegmentAnyTooth | fotografia intraoral | segmentação e FDI opcional |
| MD-OPG | panorâmica pediátrica | candidato futuro para segmentação por superfície |

Os datasets visuais não são automaticamente pareados com a coorte longitudinal. Ausência de chave comum implica bloqueio de fusão em nível de paciente.

---

## Como executar

### Google Colab — recomendado

Abra diretamente:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XnrsVU2u1Cq9igbRJHralBQrgtCYaksW)

Depois:

1. selecione um runtime com GPU para o braço visual;
2. reinicie a sessão se estiver reutilizando um runtime antigo;
3. execute as células em ordem;
4. não avance quando um gate obrigatório falhar;
5. para resultados científicos, utilize somente saídas geradas por dados reais.

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

Dependências principais declaradas em `requirements.txt`: NumPy, pandas, SciPy, scikit-learn, openpyxl, requests, matplotlib, Pillow, PyYAML, biom-format e Ultralytics.

---

## Estrutura atual do repositório

```text
OdontoCA/
├── LICENSE
├── README.md
├── requirements.txt
└── OdontoCA_v1_9_2_FLUXOGRAMA_INTERATIVO_PAN_ZOOM.ipynb
```

---

## Artefatos previstos pelo pipeline

Quando a execução integral for aprovada, o notebook prevê exportar, entre outros:

- requisitos SDD;
- especificações e resultados TDD;
- matriz de rastreabilidade SDD → TDD;
- auditorias clínicas e microbiológicas;
- inventários e QC visual;
- registros de falhas de parsing;
- predições OOF;
- métricas dos modelos;
- resultados de tuning;
- pesos `best.pt` com SHA-256;
- manifesto de reprodutibilidade;
- relatório de validação;
- `RiskAssessment` FHIR experimental;
- pacote ZIP final de resultados.

---

## Regra de promoção científica

```text
DADO REAL
   ↓
INTEGRIDADE E PROVENIÊNCIA
   ↓
SEM LEAKAGE
   ↓
VALIDAÇÃO / OOF
   ↓
TDD + ACCEPTANCE GATES
   ↓
APPROVED — PIPELINE DE PESQUISA
```

`APPROVED` significa que os requisitos do pipeline de pesquisa foram satisfeitos. **Não significa validação clínica, autorização regulatória ou desempenho comprovado para uso assistencial.**

---

## Limitações e segurança

- finalidade exclusivamente científica e educacional;
- não é dispositivo médico;
- não substitui avaliação odontológica;
- nenhuma fusão cross-cohort é permitida sem chaves comuns válidas;
- patient-disjoint visual só pode ser declarado quando existe identificação confiável de paciente;
- resultados visuais e microbiológicos devem ser considerados pendentes até execução e aprovação dos respectivos gates;
- o recurso FHIR permanece `preliminary`;
- métricas sintéticas não podem ser promovidas a resultados científicos.

---

## Licença

Consulte o arquivo [`LICENSE`](./LICENSE) deste repositório para os termos de uso do código. Datasets, artigos e pesos de terceiros permanecem sujeitos às licenças de suas respectivas fontes.
