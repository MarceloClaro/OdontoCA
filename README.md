# OdontoCA v1.9.2 — Fluxograma Interativo, SDD 5.0 e TDD 5.0
[![GitHub Repo](https://img.shields.io/badge/repo-GitHub-blue?logo=github)](https://github.com/MarceloClaro/OdontoCA)
> **Pipeline Multimodal Científico e Clínico para Predição de Risco de Cárie na Primeira Infância (*Early Childhood Caries — ECC*) ao Nível de Dente Individual.**

---

## 📌 Visão Geral

O **OdontoCA v1.9.2** é um pipeline multimodal orientado a dados reais para odontologia preventiva e translacional. Ele modela o risco de transição de dentes hígidos para cariados ($H \to C$) utilizando:

1. **Clínica Longitudinal:** Dados da coorte pediátrica (*HuangShiLab / Single-tooth ECC*, $N=89$ crianças, 20 dentes decíduos na notação FDI, 997 observações de onset com 84 eventos $H \to C$ consecutivos a $\Delta t = 1$).
2. **Microbioma Oral:** Sequenciamento de amplicon 16S do *Qiita Study 14341*, integrado via emparelhamento determinístico `SampleID ↔ BIOM`, com transformação CLR (*Centered Log-Ratio*) e seleção de features estritamente aninhada (*nested cross-validation*).
3. **Visão Computacional e Radiográfica:** 
   - Fotografia intraoral (benchmark público Zenodo `14827784`);
   - Radiografias panorâmicas pediátricas (detecção de cárie infantil e doenças dentárias de Zhang et al., Kaggle);
   - Anatomia dentária decídua e permanente (YOLOv8);
   - Algoritmo de associação geométrica lesão $\leftrightarrow$ dente baseado em **IoL (*Intersection over Lesion*)** para odontogramas automatizados.
4. **Governança e Interoperabilidade:** Recurso experimental HL7 FHIR `RiskAssessment` com status `preliminary` e bloqueio estrito de fusão ao nível de paciente entre coortes distintas (*cross-cohort guardrail*).

---

## 🏛️ Arquitetura Formal: SDD 5.0 & TDD 5.0

O projeto adota o paradigma **Specification-Driven Development (SDD)** acoplado a **Test-Driven Development (TDD)**:

* **46 Requisitos SDD:** Divididos em 11 domínios formais (Governança, Clínica, ML, Microbioma, Imagem, Fusão, FHIR, Qualidade, Reprodutibilidade, Segurança e Código).
* **58 Casos de Teste TDD:** Declarados antes da implementação e categorizados na pirâmide de testes:
  - **UNIT (20 testes):** Validação de schemas, transformadores, regras de augmentation sem inversão vertical (`flipud=0.0`) e contratos de parsing;
  - **INTEGRATION (15 testes):** Topologia FDI, integridade do pareamento com Qiita e controle de qualidade de imagens;
  - **ACCEPTANCE (23 testes):** Reprodução exata das contagens publicadas, zero vazamento de pacientes (*patient-level leakage = 0*), integridade *below-chance* (proibição de $1-AUC$) e geração do manifesto de reprodutibilidade.

---

## 🗺️ Fluxograma Interativo com Pan, Zoom e Minimapa

O notebook possui um fluxograma interativo construído com Mermaid v11 e HTML5/JS embarcado:
* **Zoom:** Roda do mouse centrado no cursor, botões `+` / `−` e atalhos de teclado `+`, `-`, `0` (ajustar) e `1` (100%);
* **Pan:** Arraste com suporte completo a *Pointer Events* (mouse, toque e caneta);
* **Navegação Rápida:** Menu seletor com salto direto entre as 16 camadas da arquitetura;
* **Minimapa:** Representação proporcional sincronizada em tempo real no canto inferior.

---

## 🦷 Aprimoramento da Identificação por Dente

A v1.9.2 incorpora inovações biológicas e topológicas:
1. **Simetria Bilateral de Antímeros:** Mapeamento dos 10 pares contralaterais decíduos ($51 \leftrightarrow 61$, $54 \leftrightarrow 64$, etc.) informando a presença e grau de cárie homóloga (`dmfs_antimero_t` e `antimero_com_carie_t`);
2. **Índice de Vulnerabilidade Salivar:** Ponderação por zona de *clearance* salivar (alto risco em incisivos superiores expostos à mamadeira vs proteção pelas glândulas sublinguais em incisivos inferiores);
3. **Associação Geométrica Lesão-Dente (IoL):**
   $$\text{IoL}(C_i, T_j) = \frac{\text{Área}(C_i \cap T_j)}{\text{Área}(C_i)}$$
   Permite desambiguação precisa de cáries interproximais, atribuindo a lesão ao dente que contém a maior fração de sua área.

---

## 🚀 Como Executar

### Opção 1: Google Colab (Recomendado com GPU T4/A100)
1. Faça o upload do arquivo `OdontoCA_v1_9_2_FLUXOGRAMA_INTERATIVO_PAN_ZOOM.ipynb` para o Google Drive / Colab;
2. Conecte um ambiente de execução com GPU (*Ambiente de Execução > Alterar tipo de ambiente de execução > GPU T4*);
3. Execute as células sequencialmente. Todos os downloads e dependências são gerenciados automaticamente.

### Opção 2: Localmente via Jupyter / VS Code
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd OdontoCA

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou no Windows:
.venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

# Inicie o Jupyter Lab / Notebook
jupyter lab
```

---

## 📄 Licença e Aviso Clínico

* **Finalidade Científica:** Este repositório destina-se estritamente à pesquisa biomédica, reprodução científica e desenvolvimento algorítmico.
* **Aviso Regulatório:** A aprovação pelo pipeline automatizado **não equivale a validação clínica ou autorização de dispositivo médico** (conforme requisito `SDD-SAFE-001`).
