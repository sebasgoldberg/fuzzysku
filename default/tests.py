#encoding=utf8
from django.test import TestCase

from models import *

class MaterialTestCase(TestCase):

    def test_consistency(self):
 
        secao = Secao.objects.create(
            cod_secao = '01',
            secao = 'ELECTRO'
        )

        secao2 = Secao.objects.create(
            cod_secao = '02',
            secao = 'ELECTRO 2'
        )

        material = Material.objects.create(
            cod_material = '0001',
            material = 'GELADEIRA',
            secao = secao
        )

        familia = Familia.objects.create(
            secao = secao2,
            cod_grupo = '0201',
            grupo = 'ELECTRO',
            cod_subgrupo = '020101',
            subgrupo = 'FRIO',
            cod_familia = '020101001',
            familia = 'GELADEIRAS'
        )

        material.familia = familia

        with self.assertRaises(SecoesNaoCoincidem):
            material.save()

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

        self.assertEqual(material.familia_sugerida,False)
        self.assertEqual(material.familia_selecionada,False)

        sugestao = Sugestao.objects.create(
            material = material,
            familia = familia
        )

        material.refresh_from_db()
        self.assertEqual(material.familia_sugerida,True)
        self.assertEqual(material.familia_selecionada,False)

        material.familia = familia
        material.save()

        material.refresh_from_db()
        self.assertEqual(material.familia_sugerida,True)
        self.assertEqual(material.familia_selecionada,True)

        sugestao.delete()

        material.refresh_from_db()
        self.assertEqual(material.familia_sugerida,False)
        self.assertEqual(material.familia_selecionada,True)

        material.familia = None
        material.save()

        material.refresh_from_db()
        self.assertEqual(material.familia_sugerida,False)
        self.assertEqual(material.familia_selecionada,False)



class SugestaoTestCase(TestCase):

    def test_sugerir(self):

        es = Elasticsearch()
        es.indices.delete(index=ES_INDEX, ignore=[400, 404])

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

        familia2 = Familia.objects.create(
            secao = secao,
            cod_grupo = '0101',
            grupo = 'ELECTRO',
            cod_subgrupo = '010101',
            subgrupo = 'FRIO',
            cod_familia = '010101002',
            familia = 'GELADEIRAS INDUSTRIAIS'
        )
        
        es.indices.refresh(index=ES_INDEX)

        sugerencias = material.sugerir()

        self.assertEqual(len(sugerencias), 2)

    def test_sugerir_respetando_secao(self):

        es = Elasticsearch()
        es.indices.delete(index=ES_INDEX, ignore=[400, 404])

        secao = Secao.objects.create(
            cod_secao = '01',
            secao = 'ELECTRO'
        )

        secao2 = Secao.objects.create(
            cod_secao = '02',
            secao = 'ELECTRO INDUSTRIAL'
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

        familia2 = Familia.objects.create(
            secao = secao2,
            cod_grupo = '0201',
            grupo = 'ELECTRO',
            cod_subgrupo = '020101',
            subgrupo = 'FRIO',
            cod_familia = '020101002',
            familia = 'GELADEIRAS INDUSTRIAIS'
        )
        
        es.indices.refresh(index=ES_INDEX)

        sugerencias = material.sugerir()

        self.assertEqual(len(sugerencias), 1)
        self.assertEqual(sugerencias[0][1], familia)


class FamiliaTestCase(TestCase):

    def test_validacoes(self):

        secao = Secao.objects.create(
            cod_secao = '01',
            secao = 'ELECTRO'
        )

        with self.assertRaises(CodigoSecaoNaoCoincide):
            familia = Familia.objects.create(
                secao = secao,
                cod_grupo = '0201',
                grupo = 'ELECTRO',
                cod_subgrupo = '010101',
                subgrupo = 'FRIO',
                cod_familia = '010101001',
                familia = 'GELADEIRAS'
            )

        with self.assertRaises(CodigoGrupoNaoCoincide):
            familia = Familia.objects.create(
                secao = secao,
                cod_grupo = '0101',
                grupo = 'ELECTRO',
                cod_subgrupo = '010201',
                subgrupo = 'FRIO',
                cod_familia = '010101001',
                familia = 'GELADEIRAS'
            )


        with self.assertRaises(CodigoSubGrupoNaoCoincide):
            familia = Familia.objects.create(
                secao = secao,
                cod_grupo = '0101',
                grupo = 'ELECTRO',
                cod_subgrupo = '010101',
                subgrupo = 'FRIO',
                cod_familia = '010102001',
                familia = 'GELADEIRAS'
            )

        familia = Familia.objects.create(
            secao = secao,
            cod_grupo = '101',
            grupo = 'ELECTRO',
            cod_subgrupo = '010101',
            subgrupo = 'FRIO',
            cod_familia = '10101001',
            familia = 'GELADEIRAS'
        )

        familia.refresh_from_db()
        self.assertEqual(familia.cod_grupo,'0101')
        self.assertEqual(familia.cod_familia,'010101001')



