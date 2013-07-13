from django.db import models

class SimpleFluid(models.Model):
    id = models.AutoField(primary_key=True, db_column=u'Id')
    name = models.CharField(db_column=u'Name', max_length=255)
    formula = models.CharField(db_column=u'Formula', max_length=255)
    cas_num = models.CharField(db_column=u'CAS_Num', max_length=30)
    mol_weight = models.FloatField(db_column=u'Mol_Wt', null=True, blank=True)
    tfp = models.FloatField(db_column=u'Tfp', null=True, blank=True)
    tb = models.FloatField(db_column=u'Tb', null=True, blank=True)
    tc = models.FloatField(db_column=u'Tc', null=True, blank=True)
    pc = models.FloatField(db_column=u'Pc', null=True, blank=True)
    vc = models.FloatField(db_column=u'Vc', null=True, blank=True)
    omega = models.FloatField(db_column=u'Omega', null=True, blank=True)
    delhf0 = models.FloatField(db_column=u'DelHf0', null=True, blank=True)
    delgf0 = models.FloatField(db_column=u'DelGf0', null=True, blank=True)
    delhb = models.FloatField(db_column=u'DelHb', null=True, blank=True)
    delhm = models.FloatField(db_column=u'DelHm', null=True, blank=True)
    vliq = models.FloatField(db_column=u'V_liq', null=True, blank=True)
    tliq = models.FloatField(db_column=u'T_liq', null=True, blank=True)
    dipole = models.FloatField(db_column=u'Dipole', null=True, blank=True)
    trange = models.FloatField(db_column=u'T_range', null=True, blank=True)
    a0 = models.FloatField(db_column=u'A0', null=True, blank=True)
    a1 = models.FloatField(db_column=u'A1', null=True, blank=True)
    a2 = models.FloatField(db_column=u'A2', null=True, blank=True)
    a3 = models.FloatField(db_column=u'A3', null=True, blank=True)
    a4 = models.FloatField(db_column=u'A4', null=True, blank=True)
    cpig = models.FloatField(db_column=u'CpIG', null=True, blank=True)
    cpliq = models.FloatField(db_column=u'CpLiq', null=True, blank=True)
    eq_num = models.IntegerField(db_column=u'Eq_Num', null=True, blank=True)
    coef0 = models.FloatField(db_column=u'C0', null=True, blank=True)
    coef1 = models.FloatField(db_column=u'C1', null=True, blank=True)
    coef2 = models.FloatField(db_column=u'C2', null=True, blank=True)
    coef3 = models.FloatField(db_column=u'C3', null=True, blank=True)
    coef4 = models.FloatField(db_column=u'C4', null=True, blank=True)
    coef5 = models.FloatField(db_column=u'C5', null=True, blank=True)
    coef6 = models.FloatField(db_column=u'C6', null=True, blank=True)
    coef7 = models.FloatField(db_column=u'C7', null=True, blank=True)
    pvpmin = models.FloatField(db_column=u'Pvp_min', null=True, blank=True)
    tmin = models.FloatField(db_column=u'T_min', null=True, blank=True)
    pvpmax = models.FloatField(db_column=u'Pvp_max', null=True, blank=True)
    tmax = models.FloatField(db_column=u'T_max', null=True, blank=True)

    # def get_absolute_url(self):
    #     return {'simple_fluid', [self.cas_num]}

    def __unicode__(self):
        return '{0} ({1}): {2}'.format(self.cas_num, self.name, self.formula)

    class Meta:
        db_table = u'simple_fluids'

