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

## O quadro é a rotina

A lista acima é só descrição. O que roda de manhã vem da barra **Recurring**
do quadro (anovabr.github.io/dashboard): a secretária lê o quadro, executa as
tarefas recorrentes endereçadas a ela, na ordem do quadro, e marca cada uma
como feita quando termina. Para mudar a rotina, mude o quadro.

Uma tarefa recorrente é da secretária quando o texto começa com 🤖, seguido de
um verbo que ela conhece e um alvo:

| Texto no quadro | O que acontece |
| :--- | :--- |
| `🤖 Publicar @anova.autismo` | publica o post do dia de `media/anova.autismo/` |
| `🤖 Responder @anova.autismo` | responde mensagens e comentários |
| `🤖 Painel https://autismo.anovasaude.org/admin.html` | lê o painel (ainda não construído — fica sem marcar) |
| `🤖 E-mail contato@anovasaude.org` | tria a caixa (ainda não construído — fica sem marcar) |
| `Pankeka Google play` (sem 🤖) | é sua: só aparece no relatório, e é cobrada se não estiver marcada |

Uma tarefa com 🤖 que ela não entende entra no relatório como "não entendi",
não é adivinhada. A regra de repetição (daily, weekdays, weekly, monthly) e a
ordem são as do próprio quadro. Se o quadro não puder ser lido, roda a lista
embutida (publicar e responder nas duas contas), para que uma queda do GitHub
não custe um post.

`tools/board-setup.py` coloca a barra Recurring neste formato; é idempotente.

