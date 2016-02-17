#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import *

COD_MATERIAL = 0
MATERIAL = 1

class Command(BaseCommand):
    help = 'Sugere familias de materiais por cada material.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        quan_sugeridos = 0
        quan_nao_sugeridos = 0

        if len(options['cod_secao']) == 0:
            materiais = Material.objects.all()
        else:
            materiais = Material.objects.filter(secoes_possiveis__cod_secao__in=options['cod_secao'])

        for material in materiais:
            sugestoes = material.sugerir()
            material.salvar_sugestoes(sugestoes)

            self.stdout.write(self.style.SUCCESS(u'Sugestão realizada para material "%s" feita com sucesso.' % material))

            for (score, familia) in sugestoes:
                self.stdout.write(self.style.SUCCESS(u'Sugestão [%s]: "%s".' % (score, familia) ))

            if len(sugestoes) > 0:
                quan_sugeridos = quan_sugeridos + 1
            else:
                self.stdout.write(self.style.WARNING(u'Sem sugestões para material "%s".' % material))
                quan_nao_sugeridos = quan_nao_sugeridos + 1

        self.stdout.write(self.style.SUCCESS(u'Resultados: [Sugeridos: %s] [Sem sugestões: %s]' %
            (quan_sugeridos, quan_nao_sugeridos) ))
        quan_tot = quan_sugeridos + quan_nao_sugeridos
        if quan_tot <> 0:
            porcentagem_sugeridos = float((quan_sugeridos)*100)/quan_tot
        else:
            porcentagem_sugeridos = 0
        self.stdout.write(self.style.SUCCESS(u'Porcentagem de sugeridos %s%%.' % porcentagem_sugeridos ))
