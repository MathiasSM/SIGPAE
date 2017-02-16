from django.test import TestCase
from ocr.models import *

class OrganoAcademicoSingle(TestCase):
    """Un único órgano presente"""

    nombre='División de Ciencias Básicas'
    tipo='Divi'
    def setUp(self):
        self.only = OrganoAcademico.objects.create(nombre=self.nombre,tipo=self.tipo)

    def test_printsOk(self):
        """Model prints as it should"""
        self.assertEqual(self.only.__str__(),self.nombre)


class UnidadAcademicaSingle(TestCase):
    """Un único órgano presente"""

    nombreD='Departamento de Ciencias Repetidas'
    nombreO='División de Ciencias Básicas'
    tipoO='Divi'

    def setUp(self):
        self.org = OrganoAcademico.objects.create(nombre=self.nombreO,tipo=self.tipoO)
        self.org.save()
        self.dep = UnidadAcademica.objects.create(nombre=self.nombreD)
        self.dep.save()
        self.dep.organo.add(self.org)

    def test_printsOk(self):
        """Model prints as it should"""
        self.assertEqual(self.dep.__str__(),self.nombreD)

    def test_organoCorrecto(self):
        """Setea correctamente el organo al que está adscrito"""
        self.assertTrue(self.dep.organo.filter(nombre=self.org.nombre).exists())

    def test_unidadCorrectamenteEnOrgano(self):
        """Setea correctamente la unidad adscrita al organo"""
        self.assertTrue(self.org.adscritoa.filter(nombre=self.dep.nombre).exists())
