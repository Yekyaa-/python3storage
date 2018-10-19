def myEgcd(a,b):
    qJust = 15
    rJust = 30
    sJust = 30
    tJust = 30
    iJust = 5
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a
    i = 0
    d = '{0}\t{1}{2}{3}{4}'
    q = 0
    print(d.format('Index  '.rjust(iJust),'Quotient q_i-1'.rjust(qJust),'Remainder r_i'.rjust(rJust),'s_i    '.rjust(sJust),'t_i    '.rjust(tJust)))
    print(d.format(str(i).rjust(iJust), ' '.rjust(qJust), str(a).rjust(rJust), str(old_s).rjust(sJust), str(old_t).rjust(tJust)))
    i = i + 1
    print(d.format(str(i).rjust(iJust), ' '.rjust(qJust), str(b).rjust(rJust), str(s).rjust(sJust), str(t).rjust(tJust)))
    while r != 0 :
        i = i + 1
        qi_1 = old_r//r
        zero = '{0} / {1} = {2}'.format(old_r, r, qi_1)
        ri = old_r - qi_1*r
        one = '{0} - {1} * {2} = {3}'.format(old_r, qi_1, r, ri)
        si = old_s - qi_1*s
        two = '{0} - {1} * {2} = {3}'.format(old_s, qi_1, s, si)
        ti = old_t - qi_1*t
        three = '{0} - {1} * {2} = {3}'.format(old_t, qi_1, t, ti)
        print(d.format(str(i).rjust(iJust), zero.rjust(qJust), one.rjust(rJust), two.rjust(sJust), three.rjust(tJust)))
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    print('The gcd of {0} and {1} is {2}.'.format(a,b,old_r))
    print('Bezout coefficients : {0} and {1} because ({0} * {2}) + ({1} * {3}) = {4}.'.format(old_s,old_t,a,b,old_s*a+old_t*b))
    print('Quotients of {0} and {1} divided by {2} are {3} and {4}.'.format(a,b,old_r,abs(s),abs(t)))
    print()
    return old_r
myEgcd(240,46)
myEgcd(101,17)
myEgcd(myEgcd(64128064,513537536512), 24024)
