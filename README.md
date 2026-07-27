# PAWS.VICA — site de uma página

Site institucional da [@paws.vica](https://www.instagram.com/paws.vica): passeio com cães,
pet sitter e adestramento em **Laranjeiras, Zona Sul do Rio de Janeiro**.

HTML + CSS + JavaScript puro, sem build step e sem dependências externas.
É só abrir o `index.html` ou publicar a pasta inteira.

## O que precisa ser preenchido

Tudo que muda está no objeto `CONFIG`, no começo do `<script>` em `index.html`:

| Campo | O que é | Estado |
|---|---|---|
| `CONFIG.whatsapp` | Número com código do país e DDD, só dígitos (ex.: `5521998877665`) | ⚠️ **placeholder** |
| `CONFIG.whatsappDisplay` | Como o número aparece escrito na página | ⚠️ **placeholder** |
| `CONFIG.instagram` | Link do perfil | ✅ preenchido |
| `CONFIG.services` | Nome, descrição e horários de cada serviço | ✅ preenchido |
| `CONFIG.diasFechados` | Dias da semana sem atendimento (`0` = domingo) | ✅ domingo |
| `CONFIG.mesesAdiante` | Quantos meses a agenda abre para frente | ✅ 3 meses |

Os **preços** estão como `R$ XX` no HTML, na seção *Serviços* — procure por `R$ XX`.

Enquanto o WhatsApp não for configurado, a última etapa do agendamento mostra um aviso,
copia a mensagem para a área de transferência e abre o Direct do Instagram.
Assim que o número real entrar no `CONFIG`, o botão passa a abrir o WhatsApp
com a mensagem já escrita — sem mais nenhuma mudança no código.

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

Qualquer hospedagem de arquivos estáticos serve. Com GitHub Pages, basta apontar
para a branch e a raiz do repositório. Para testar localmente:

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
