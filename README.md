# PAWS.VICA — site de uma página

Site institucional da [@paws.vica](https://www.instagram.com/paws.vica): passeio com cães,
pet sitter e adestramento em **Laranjeiras, Zona Sul do Rio de Janeiro**.

HTML + CSS + JavaScript puro, sem build step e sem dependências externas.
É só abrir o `index.html` ou publicar a pasta inteira.

## O que precisa ser preenchido

Tudo que muda está no objeto `CONFIG`, no começo do `<script>` em `index.html`:

| Campo | O que é | Estado |
|---|---|---|
| `CONFIG.whatsapp` | Número com código do país e DDD, só dígitos | ✅ `5521996150112` |
| `CONFIG.whatsappDisplay` | Como o número aparece escrito no rodapé | ✅ `+55 21 99615-0112` |
| `CONFIG.instagram` | Link do perfil | ✅ preenchido |
| `CONFIG.services` | Nome, descrição e horários de cada serviço | ✅ preenchido |
| `CONFIG.diasFechados` | Dias da semana sem atendimento (`0` = domingo) | ✅ domingo |
| `CONFIG.mesesAdiante` | Quantos meses a agenda abre para frente | ✅ 3 meses |

Os **preços** estão como `R$ XX` no HTML, na seção *Serviços* — procure por `R$ XX`.

O WhatsApp já está ligado: a última etapa do agendamento abre uma conversa com a Vica
já com serviço, data, horário e dados do cão escritos na mensagem.

Se o número for apagado ou trocado por um placeholder (qualquer coisa com `X`), a
página detecta sozinha, mostra um aviso, copia a mensagem para a área de transferência
e cai no Direct do Instagram em vez de gerar um link `wa.me` quebrado.

## A agenda

A disponibilidade do calendário é **fictícia, mas determinística**: cada data sempre
devolve o mesmo resultado, em qualquer navegador ou visita. Domingos e datas passadas
ficam sempre bloqueados; cerca de 18% dos dias aparecem como lotados e o restante se
divide entre "vários horários" e "últimos horários".

A regra vive em `dayInfo()`. Para plugar uma agenda real (Google Calendar, Calendly,
backend próprio), basta substituir essa função — ela é o único ponto que decide
disponibilidade, e o resto da interface continua igual.

## Estrutura

```
index.html          página inteira (marcação, estilos e script)
assets/
  fonts.css         @font-face das fontes auto-hospedadas
  fonts/            Archivo Black, Inter e Caveat (woff2, subsets latin)
  vitoria-banana.jpg
  pancake.jpg
  face-vitoria.jpg  face-pancake.jpg  face-banana.jpg
  og-image.jpg      cartão 1200×630 da prévia de link
README.md
```

## Marca

Cores tiradas direto do feed do Instagram:

- `#E390A4` rosa da marca — usado em fundos e preenchimentos
- `#DA6B86` mesma matiz, escurecida para títulos sobre creme (contraste AA)
- `#FDF7F7` creme de fundo
- `#16110F` tinta, quase preto, inspirado no pelo da Pancake e do Banana

Tipografia: **Archivo Black** nos títulos (a mais próxima do wordmark do perfil),
**Inter** no texto corrido e **Caveat** nas anotações à mão.

## Publicando

No ar em **https://anovabr.github.io/vica/** via GitHub Pages
(Settings → Pages → Deploy from a branch → `main` → `/ (root)`).
Cada push para `main` republica sozinho.

Se o endereço mudar — domínio próprio, por exemplo — troque a URL em três lugares
no `<head>` do `index.html`: `canonical`, `og:url` e `og:image` (mais `twitter:image`
e o `url`/`image` do JSON-LD). Precisam ser **URLs absolutas**: os robôs que montam
a prévia do link no WhatsApp e no Instagram não resolvem caminho relativo.

Para testar localmente:

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

Servir por HTTP (e não abrir o arquivo direto) é importante para as fontes
carregarem — o navegador bloqueia fontes via `file://`.

## Verificações já feitas

- Sem rolagem horizontal de 320px a 1440px
- Contraste AA em todos os textos
- Modal com foco preso, retorno de foco, fechamento por `Esc` e calendário
  navegável pelas setas do teclado
- `prefers-reduced-motion` respeitado
- Sem erros de JavaScript no console
