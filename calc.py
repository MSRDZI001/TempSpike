# for calculating stuff

def toResistance(values):
    #Calculates restance based of Justin Peads Excel document.
    #Determines the estimated resistance,
    #circuit parameters
    res = 12
    s_res = 220
    feedback_resup = 100000
    feedback_reslow = 10000
    ADC_Volt = 3.3
    Sensor_Volt=5
    max_value = 2**res-1
    
    val_Adjustment_constant = 1.9 #ADJUST THIS VALUE TO GET CORRECT RESISTANCE. The default seems to work the best. Still cannot work out why its always double the value.
    
    resistances = []
    
    #early calcs
    nominal_gain = 1/(feedback_reslow/(feedback_resup+feedback_reslow))
    
    for value in values:
        if(value == 65535):
            resistances.append(0)
        else:
            v_out = ADC_Volt * value / max_value
            nom_gain = Sensor_Volt- v_out/nominal_gain
            est_res = nom_gain/(v_out/(nominal_gain*s_res))
            resistances.append(round(est_res*2,2))
    
    return resistances

def toTemp(values):
    #Determines tempreture from tmp235, only takes arrays. 
    #Defined by tmp235 datasheet range -40 to +100
    Voffs = 500
    Tc = 10
    Tinfl = 0
    res =2**12
    ADC_volt = 3300
    
    temps = []
    Ta = 0
    for value in values:
        
        Vout = value/(res) * ADC_volt
        if(Vout > 2000):
            Ta = 0
        
        else:
            Ta = (Vout - Voffs)/Tc + Tinfl
        
        temps.append(round(Ta,2))
    
    return temps
    