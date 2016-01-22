from django.test import TestCase

from models import *

# Create your tests here.
class SugestaoTestCase(TestCase):
    
    def test_signal(self):

        secao = Secao.objects.create(
            cod_secao = '01',
            secao = 'ELECTRO'
        )

        material = Material.objects.create(
            cod_material = '0001',
            material = 'GELADEIRA',
            secao = secao
        )

        familia = Familia.objects.create(
            secao = secao,
            cod_grupo = '0101',
            grupo = 'ELECTRO',
            cod_subgrupo = '010101',
            subgrupo = 'FRIO',
            cod_familia = '010101001',
            familia = 'GELADEIRAS'
        )

        sugestao = Sugestao.objects.create(
            material = material,
            familia = familia
        )

        material.refresh_from_db()
        self.assertEqual(material.familia, None)
        self.assertEqual(material.familia_sugerida, True)
        self.assertEqual(material.familia_selecionada, False)
        self.assertEqual(material.multiplas_familias_selecionadas, False)

        sugestao.selecionado = True

        sugestao.save()

        material.refresh_from_db()
        self.assertEqual(material.familia, sugestao.familia)
        self.assertEqual(material.familia_sugerida, True)
        self.assertEqual(material.familia_selecionada, True)
        self.assertEqual(material.multiplas_familias_selecionadas, False)

        sugestao.selecionado = False

        sugestao.save()

        material.refresh_from_db()
        self.assertEqual(material.familia, None)
        self.assertEqual(material.familia_sugerida, True)
        self.assertEqual(material.familia_selecionada, False)
        self.assertEqual(material.multiplas_familias_selecionadas, False)


        sugestao.delete()

        material.refresh_from_db()
        self.assertEqual(material.familia, None)
        self.assertEqual(material.familia_sugerida, False)
        self.assertEqual(material.familia_selecionada, False)
        self.assertEqual(material.multiplas_familias_selecionadas, False)

