# Rotina

The order below is the order it runs. The agent works top to bottom, records
what happened, and finishes by producing the report.

**Tom de voz:** profissional, sempre em português. Não dar orientação clínica
individual — encaminhar ao link do perfil ou ao e-mail de contato.

---

## Diária — 07:00

1. **Instagram `anova.autismo` — publicar**
   Post do dia. Media must be a public https URL.

2. **Instagram `anova.autismo` — responder mensagens**
   Answer what can be answered simply. Anything outside the 24-hour window,
   or that needs a real decision, goes to the report instead.

3. **Painel `autismo.anovasaude.org/admin.html`**
   Novas avaliações, novos cadastros.

4. **Painel anovasaude — avaliações realizadas**

5. **Painel anovasaude — novos profissionais cadastrados**

6. **Instagram `pankeka.app` — publicar**

7. **E-mail `contato@anovasaude.org`**
   Triar mensagens novas. Responder as dúvidas gerais com o texto padrão;
   separar o resto para você.

8. **Relatório**
   Everything above, in this order, with what needs you at the end.

## De hora em hora

- **Instagram — verificar mensagens e comentários** nas duas contas.
  Só relata se houver algo; silêncio quando não há nada novo.

---

## Board vs. this file

The dashboard's `repeat: daily` tasks are the source of truth, and there are
only four of them:

| Board task | Section |
| :--- | :--- |
| Post instagram | ANOVA / anova autismo |
| Admin `https://autismo.anovasaude.org/admin.html` | ANOVA / anova autismo |
| Admin `https://anovasaude.org/admin` | ANOVA / anova saude |
| Pankeka Google play | others |

Four things you described are **not** on the board, and one board item is not
what you described. Until this is settled the agent follows the list above,
because that is what is written down:

- **"Pankeka Google play"**, not an Instagram post for `pankeka.app`. These are
  different jobs — one is the Play Console, one is publishing. Which is it?
- **Replying to Instagram messages** — described, not on the board.
- **The hourly Instagram check** — described, not on the board.
- **`contato@anovasaude.org`** — described, not on the board.
- **New professionals registered** may be part of the anovasaude admin task
  rather than a step of its own.

## Ainda não definido

- Onde ficam as imagens dos posts (Instagram busca por URL pública).
- Como o agente lê os painéis — API do próprio sistema é bem melhor que
  automação de navegador. Ver `docs/paineis.md`.
- Provedor do e-mail `contato@anovasaude.org`.
- Texto padrão para as dúvidas gerais.
- Por onde chega o relatório: e-mail, WhatsApp ou arquivo no repositório.
