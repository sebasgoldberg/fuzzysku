#encoding=utf8
from django.core.management.base import BaseCommand, CommandError
from default.models import Material, SelecaoRealizadaException

COD_MATERIAL = 0
MATERIAL = 1

class Command(BaseCommand):
    help = 'Sugere familias de materiais por cada material.'

    def add_arguments(self, parser):
        parser.add_argument('cod_secao', nargs='*')

    def handle(self, *args, **options):

        quan_sugeridos = 0
        quan_nao_sugeridos = 0
        quan_selecao_realizada = 0

        if len(options['cod_secao']) == 0:
            materiais = Material.objects.all()
        else:
            materiais = Material.objects.filter(secao__cod_secao__in=options['cod_secao'])

        for material in materiais:
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
        if quan_tot <> 0:
            porcentagem_sugeridos = float((quan_sugeridos+quan_selecao_realizada)*100)/quan_tot
        else:
            porcentagem_sugeridos = 0
        self.stdout.write(self.style.SUCCESS(str('Porcentagem de sugeridos %s%%.' % str(porcentagem_sugeridos) ).decode('ascii','ignore')))
