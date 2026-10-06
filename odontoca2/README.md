# Panoramica AI / OdontoCA 2.0 — SDD/TDD radiográfico

Este módulo adiciona uma camada auditável para inferência em radiografias panorâmicas.

## Ordem do pipeline

1. controle de qualidade;
2. detecção/segmentação de dentes;
3. FDI contextual;
4. restauração/endodontia;
5. cárie e outros achados;
6. anatomia;
7. motor de consistência;
8. explicabilidade;
9. revisão humana;
10. laudo estruturado.

## Invariantes

- Score do modelo não é probabilidade clínica.
- Estrutura anatômica não segmentada não pode ser reportada como ausente.
- Todo achado precisa de localização e versão do modelo.
- Achado dentário precisa referenciar uma instância dentária.
- Número de achados declarado deve coincidir com o número de registros.
- Conflito cárie × restauração/endodontia exige revisão humana.
- Grad-CAM só pode ser rotulado como tal com proveniência do modelo, camada e alvo.
- CASE_117 é caso sentinela de regressão e não deve compor o treino.
- Ground truth clínico permanece pendente até consenso profissional.

## CASE_117

Imagem original: `117.jpg`  
SHA-256: `871bb224a0d93e394704dc9756cd60185b54b65103128d442f5ab404ab179bfb`

O caso reproduz a classe de falhas observada na auditoria: subdetecção mandibular, FDI incompleto, contagem de achados inconsistente e interpretação inadequada de falha de segmentação anatômica.

A imagem clínica não é incluída neste branch; o teste guarda apenas o identificador criptográfico e as regras de segurança. Para execução visual local, forneça o arquivo original com o SHA-256 acima em `tests/regression/case_117/117.jpg`.

## Execução

```bash
cd odontoca2
python -m pip install -e ".[test]"
pytest -q
```
