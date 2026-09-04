"""A worked example of the daily report, following the real routine order.

    python -m secretary.demo_report

The numbers here are invented — this exists so the format can be judged and
corrected before the agent runs for real.
"""

from datetime import datetime

from .report import Report


def build() -> Report:
    r = Report(datetime(2026, 9, 3, 7, 41), titulo="Relatório da secretária")

    ig = r.section("Instagram · anova.autismo")
    r.feito(ig, "Publicação às 07:04",
            'Carrossel, 3 imagens — "Rotina visual: por que funciona"',
            "https://www.instagram.com/p/DAbC123xyz/")
    r.feito(ig, "5 mensagens diretas respondidas",
            "3 sobre idade de avaliação, 1 sobre convênio, 1 agradecimento.\n"
            "Todas encaminhadas ao link do perfil para agendamento.")
    r.atencao(ig, "1 mensagem fora da janela de resposta",
              "@carlos.ferreira, há 3 dias: \"Vocês atendem em Niterói?\"\n"
              "O Instagram não permite mais resposta automática nesta conversa.")
    r.feito(ig, "2 comentários respondidos", "Nenhum comentário exigiu moderação.")

    adm = r.section("Painel · autismo.anovasaude.org")
    r.feito(adm, "7 novas avaliações registradas",
            "5 concluídas, 2 em andamento. Faixa etária 4–11 anos.")
    r.feito(adm, "4 novos cadastros de responsáveis")
    r.atencao(adm, "2 avaliações interrompidas na etapa 3",
              "Mesma etapa nos dois casos — pode indicar problema no formulário.")

    prof = r.section("Painel · profissionais")
    r.feito(prof, "3 profissionais cadastrados",
            "2 psicólogas (CRP verificado), 1 fonoaudióloga.")
    r.atencao(prof, "1 cadastro sem número de conselho",
              "Cadastro retido, aguardando sua conferência antes da aprovação.")

    pk = r.section("Instagram · pankeka.app")
    r.feito(pk, "Publicação às 07:22",
            'Imagem única — "Novidade: modo offline"',
            "https://www.instagram.com/p/DAbC456uvw/")
    r.feito(pk, "3 mensagens diretas respondidas",
            "2 dúvidas de uso, 1 relato de erro no Android.")

    mail = r.section("E-mail · contato@anovasaude.org")
    r.feito(mail, "11 mensagens novas triadas",
            "6 dúvidas gerais respondidas com o texto padrão.\n"
            "3 arquivadas como divulgação.")
    r.atencao(mail, "2 mensagens deixadas para você",
              "1 proposta de parceria (Instituto Reviver)\n"
              "1 solicitação de imprensa com prazo até sexta-feira")

    return r


if __name__ == "__main__":
    print(build().render())
