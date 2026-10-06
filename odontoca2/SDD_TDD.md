# SDD/TDD — Panoramica AI / OdontoCA 2.0

## SDD

### Objetivo
Produzir inferência odontológica automatizada auditável, mantendo detecção, identificação, tratamento prévio, patologia, anatomia, explicabilidade e revisão humana como etapas distintas.

### Invariantes
- INV-01: FDI só pode ser associado a uma instância dentária.
- INV-02: todo achado deve possuir localização.
- INV-03: achado dentário deve possuir referência de dente.
- INV-04: contagem declarada = número de registros.
- INV-05: não segmentado ≠ ausente.
- INV-06: score ≠ probabilidade clínica.
- INV-07: conflito cárie/restauração/endodontia exige revisão.
- INV-08: versão do modelo deve ser registrada.
- INV-09: correção humana deve ser auditável.
- INV-10: fixture de teste não deve entrar no treino.
- INV-11: Grad-CAM exige proveniência real.

## TDD

Testes mínimos:
- geometria válida de bounding box;
- FDI dentro do conjunto permitido;
- não segmentação anatômica nunca convertida em ausência;
- bloqueio para contagem inconsistente de achados;
- bloqueio de referência dentária inexistente;
- FDI duplicado bloqueado;
- conflito cárie/restauração/endodontia marcado para revisão;
- Grad-CAM com método/camada/classe/detecção/versionamento;
- heatmap normalizado;
- redação de diagnóstico autônomo proibida;
- CASE_117 não incluído no treino;
- ground truth do CASE_117 permanece pendente até consenso profissional.

## Critério de promoção
Nenhum release deve ser promovido se houver falha em invariantes de segurança ou regressão do CASE_117.
