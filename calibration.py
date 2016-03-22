from gencal import gencal
from gaincal import gaincal
from setjy import setjy
from bandpass import bandpass
from applycal import applycal

__all__ = ['ant_correction', 'flux_density_scale', 'phase_cal_init',
           'delay_cal', 'bandpass_cal', 'complex_gain_cal', 'cal_all']


def ant_correction(vis, caltable_out):
    gencal(vis=vis, caltable=caltable_out, caltype='antpos')


def flux_density_scale(vis, **kwargs):
    setjy(vis=vis, **kwargs)


def phase_cal_init(vis, caltable_out, caltable_in=None, **kwargs):
    gaincal(vis=vis, caltable=caltable_out, gaintable=caltable_in,
            gaintype='G', calmode='p', solint='int', **kwargs)


def delay_cal(vis, caltable_out, caltable_in=None, **kwargs):
    gaincal(vis=vis, caltable=caltable_out, gaintable=caltable_in,
            gaintype='K', solint='inf', combine='scan', **kwargs)


def bandpass_cal(vis, caltable_out, caltable_in=None, **kwargs):
    bandpass(vis=vis, caltable=caltable_out, solnorm=True, combine='scan',
             solint='inf', bandtype='B', gaintable=caltable_in, **kwargs)


def complex_gain_cal(vis, caltable_out, caltable_in=None, **kwargs):
    gaincal(vis=vis, caltable=caltable_out, solint='inf', gaintype='G',
            calmode='ap', solnorm=False, gaintable=caltable_in, **kwargs)


def apply_calibration(vis, caltables, **kwargs):
    applycal(vis, gaintable=caltables)


def cal_all(vis, cal_order='afpdbc', caltables_in=None,
            apply_cal=False, apply_cal_kwd=None):
    """Loop over and execute calibration following the given order.

    Parameters
    ----------
    vis : str
        Visibility measurement set
    cal_order : str, choices from {a,f,p,d,b,c,}
        String keyword for calibration order.
            a=ant_correction, f=flux_density_scale, p=phase_cal_init,
            d=delay_cal, b=bandpass_cal, c=complex_gain_cal
        Example: 'dbc' will do delay, bandpass and complex gain calibration
    apply_cal: bool
        Apply calibration if True
    apply_cal_kwd: dict
        Keyword arguments to pass to `apply_calibration`
    Returns
    -------

    """
    cal_func = dict(a=ant_correction, f=flux_density_scale, p=phase_cal_init,
                    d=delay_cal, b=bandpass_cal, c=complex_gain_cal)
    caltb_suffix = dict(a='.antpos', p='.G0', d='.K0', b='.B0', c='.G1')
    if caltables_in is None:
        caltables_in = []
    for idx in cal_order:
        if idx == 'f':
            cal_func[idx](vis)
        else:
            caltable_out = vis.replace('.ms', caltb_suffix[idx])
            if idx == 'a':
                cal_func[idx](vis, caltable_out)
            else:
                cal_func[idx](vis, caltable_out, caltables_in)
            caltables_in.append(caltable_out)
    if apply_cal:
        apply_calibration(vis, caltables_in, **apply_cal_kwd)
