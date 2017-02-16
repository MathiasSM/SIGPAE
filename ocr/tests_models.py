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


class ProgramaSingle(TestCase):
    """Un único programa presente"""

    nombreO='División de Ciencias Básicas'
    tipoO='Divi'
    nombreD='Departamento de Ciencias Repetidas'

    codigo = "CI3131"
    denominacion = "Aprendiendo Django a la fuerza"
    fecha_periodo = "2"
    fecha_año = 1999
    horas_teoria = 12
    horas_practica = 9
    horas_laboratorio = 2
    creditos = 8

    def setUp(self):
        self.org = OrganoAcademico.objects.create(nombre=self.nombreO,tipo=self.tipoO)
        self.org.save()

        self.dep = UnidadAcademica.objects.create(nombre=self.nombreD)
        self.dep.save()
        self.dep.organo.add(self.org)

        self.pro = Programa.objects.create(
            codigo=             self.codigo,
            denominacion=       self.denominacion,
            fecha_periodo=      self.fecha_periodo,
            fecha_año=          self.fecha_año,
            horas_teoria=       self.horas_teoria,
            horas_practica=     self.horas_practica,
            horas_laboratorio=  self.horas_laboratorio,
            creditos=           self.creditos,
            departamento=       self.dep
        )
        self.pro.save()

    def test_printsOk(self):
        """Model prints as it should"""
        self.assertEqual(self.pro.__str__(), self.pro.codigo + " (" + self.pro.PERIODOS[int(self.pro.fecha_periodo)][1] + " " + str(self.pro.fecha_año) + ")")

    def test_depCorrecto(self):
        """Setea correctamente el departamento que la regula"""
        self.assertEqual(self.pro.departamento, self.dep)
