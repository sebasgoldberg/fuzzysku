#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Material, SelecaoRealizadaException

COD_MATERIAL = 0
MATERIAL = 1

class Command(BaseCommand):
    help = 'Sugere familias de materiais por cada material.'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        quan_sugeridos = 0
        quan_nao_sugeridos = 0
        quan_selecao_realizada = 0

        for material in Material.objects.all():
            try:
                sugestoes = material.sugerir()
                material.salvar_sugestoes(sugestoes)

                self.stdout.write(self.style.SUCCESS(str('Sugestão realizada para material "%s" feita com sucesso.' % material).decode('ascii','ignore')))

                for (score, familia) in sugestoes:
                    self.stdout.write(self.style.SUCCESS(str('Sugestão [%s]: "%s".' % (score, familia) ).decode('ascii','ignore')))
                
                if len(sugestoes) > 0:
                    quan_sugeridos = quan_sugeridos + 1
                else:
                    self.stdout.write(self.style.WARNING(str('Sem sugestões para material "%s".' % material).decode('ascii','ignore')))
                    quan_nao_sugeridos = quan_nao_sugeridos + 1

            except SelecaoRealizadaException:
                self.stdout.write(self.style.ERROR(str('Material "%s" já tem seleção realizada.' % material).decode('ascii','ignore')))
                quan_selecao_realizada = quan_selecao_realizada + 1

        self.stdout.write(self.style.SUCCESS(str('Resultados: [Sugeridos: %s] [Sem sugestões: %s] [Já selecionados: %s]' %
            (quan_sugeridos, quan_nao_sugeridos, quan_selecao_realizada) ).decode('ascii','ignore')))
        quan_tot = quan_sugeridos + quan_nao_sugeridos + quan_selecao_realizada
        self.stdout.write(self.style.SUCCESS(str('Porcentagem de sugeridos %s%%.' % str(float((quan_sugeridos+quan_selecao_realizada)*100)/quan_tot) ).decode('ascii','ignore')))
