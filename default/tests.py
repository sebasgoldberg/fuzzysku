#encoding=utf8
from django.test import TestCase

from models import *

class MaterialTestCase(TestCase):

    def test_mesma_secao_familia(self):

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

    def test_secoes_possiveis_con_valor_de_secao(self):
        
        secao = Secao.objects.create(
            cod_secao = '01',
            secao = 'ELECTRO'
        )

        material = Material.objects.create(
            cod_material = '0001',
            material = 'GELADEIRA',
            secao = secao
        )

        material.refresh_from_db()
        self.assertEqual(material.secoes_possiveis, secao.cod_secao)

    def test_secao_familia_in_secoes_possiveis(self):
        
        es = Elasticsearch()
        es.indices.delete(index=ES_INDEX, ignore=[400, 404])

        secao = Secao.objects.create(
            cod_secao = '01',
            secao = 'ELECTRO'
        )

        secao2 = Secao.objects.create(
            cod_secao = '02',
            secao = 'ELECTRO 2'
        )

        secao3 = Secao.objects.create(
            cod_secao = '03',
            secao = 'ELECTRO 3'
        )

        material = Material.objects.create(
            cod_material = '0001',
            material = 'GELADEIRA',
            secoes_possiveis = Material.to_secoes_posiveis([secao, secao2])
        )

        material.refresh_from_db()
        secoes_possiveis = material.get_secoes_possiveis()
        self.assertEqual(len(secoes_possiveis), 2)
        self.assertIn(secao, secoes_possiveis)
        self.assertIn(secao2, secoes_possiveis)

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
            cod_familia = '020101001',
            familia = 'GELADEIRAS'
        )

        familia3 = Familia.objects.create(
            secao = secao3,
            cod_grupo = '0301',
            grupo = 'ELECTRO',
            cod_subgrupo = '030101',
            subgrupo = 'FRIO',
            cod_familia = '030101001',
            familia = 'GELADEIRAS'
        )

        material.familia = familia3

        with self.assertRaises(SecoesNaoCoincidem):
            material.save()

        material.familia = familia
        material.save()
        material.refresh_from_db()
        self.assertEqual(material.secao, familia.secao)

        material.familia = familia2
        material.save()
        material.refresh_from_db()
        self.assertEqual(material.secao, familia2.secao)

        material.refresh_from_db()
        secoes_possiveis = material.get_secoes_possiveis()
        self.assertEqual(len(secoes_possiveis), 2)
        self.assertIn(secao, secoes_possiveis)
        self.assertIn(secao2, secoes_possiveis)

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

    def test_sugerir_respetando_secoes(self):

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

        secao3 = Secao.objects.create(
            cod_secao = '03',
            secao = 'ELECTRO INDUSTRIAL'
        )

        material = Material.objects.create(
            cod_material = '0001',
            material = 'GELADEIRA',
            secoes_possiveis = '01 02'
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
        
 
        familia3 = Familia.objects.create(
            secao = secao3,
            cod_grupo = '0301',
            grupo = 'ELECTRO',
            cod_subgrupo = '030101',
            subgrupo = 'FRIO',
            cod_familia = '030101002',
            familia = 'GELADEIRAS INDUSTRIAIS'
        )
        
        es.indices.refresh(index=ES_INDEX)

        sugerencias = material.sugerir()

        self.assertEqual(len(sugerencias), 2)
        self.assertIn(familia, [ x[1] for x in sugerencias ])
        self.assertIn(familia2, [ x[1] for x in sugerencias ])





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



