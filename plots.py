from numpy import array, empty_like, amin, amax
from numpy import put, empty, zeros, ogrid, mgrid, atleast_2d, linspace, meshgrid, log10, log
from pylab import show, imshow, contour, gca, scatter, xlabel, ylabel
from matplotlib.ticker import LogLocator

XX=array([6.169037046118459,
1.2652658707139501,
2.5265390695088565,
2.8905433376156844,
4.210093513536358,
2.9841789812083808,
3.678508409934936,
2.1478813790170017,
1.8625669641140268,
1.0200015971343934,
1.2326036891978005,
0.993640412204898,
1.9491001468763671,
1.7047765803653303,
2.711920893710764,
2.0846930271146786,
1.4384559085934914,
1.9744793926330246,
1.6937677315385267,
1.7207437729041142,
1.3040379345611939,
1.1547189334139012,
0.983064068527407,
1.1621998960021047,
1.1620161244687142,
1.2038452357039027,
1.003594832408878,
1.4288697832154313,
1.4107927488229315,
1.437327256016331,
1.2888283314691744,
0.6938023025293069,
0.8374285404416131,
1.06032686054228,
1.5298335634227176,
1.4295242017632015,
1.1618251771126964,
0.8288637040161344,
0.9830641790380472,
1.0739073157242018,
1.1547190784200911,
0.7726277016761303,
0.981568053427395,
1.0379094942893117,
0.951995347590519,
1.4175927455489008,
0.9718665081389398,
1.406547631520551,
1.1784217098887626,
1.2684614593912238,
0.8840761211169412,
0.9119723202279918,
0.41947551092842456,
0.7306382264229961,
0.5931974248696301,
0.929987080786315,
0.686619028908907,
0.6715694644592382,
0.31973965369921975,
0.269434024885641,
0.5956911294308069,
0.6812247340859253,
0.4628597501815189,
1.014460238602395,
1.1711638677526979,
1.5336386865534988,
1.0232863266910397,
0.9756533578331561,
0.9830640832428694,
1.1547190245157148,
1.0551620322006876,
0.7726278061780678,
1.0393472715175656,
0.7683146686337577,
1.112912139722843,
0.7683146923281254,
1.1707267926179454,
0.6917637376624723,
1.2558917472783646,
0.751072026192452,
0.8356744167198507,
0.6469096593950195,
0.6514110919122572,
0.6469096662635568,
0.38731931878435144,
0.45295927728506763,
0.4072506905250332,
0.1694476920255073,
0.18621958886885567,
0.41704744569951013,
0.5212032670585465,
0.5545982962679074,
0.7906930183457497,
0.8830031183082336,
0.9652443365633423,
1.0052129918078527,
1.0150357078174514,
0.7686742247293419,
0.9830642981534663,
1.1547190875553046,
1.0393473986095163,
0.9830641895008019,
0.7686742023701421,
1.1442468076672418,
0.9084538632660422,
1.0379095337975786,
0.8268876267337688,
1.1578850429406091,
0.9655207006406468,
1.1707267600314997,
0.7510721332992232,
0.9655206059495187,
0.843500333645073,
0.5969616939735344,
0.5796942913371634,
0.6355775729502664,
0.4194756435269064,
0.4728732509903825,
0.34539675792547314,
0.44831402024821493,
0.34691781351680184,
0.3906225315433654,
0.21267801153419016,
0.19044004040024148,
3.2708461366849747E-8,
0.10436754129169132,
0.2607075655833101,
0.4011141314274156,
0.45987376235115907,
0.5224830858139495,
0.6252114895692656,
0.5425457518172901,
0.7906930807503747,
1.005213056191467,
0.9058541946110394,
0.7686742180764681,
0.8335582462548861,
0.9039987863502672,
1.055162107128536,
0.7686742404105789,
0.9819006299377976,
1.1442468671859776,
0.9830642290137837,
1.0379095848543132,
0.7683147363078446,
0.9987194575410865,
0.577832322887434,
0.9766406382586841,
0.6221504756694642,
1.0186582641298365,
0.906075231005554,
0.635718250341113,
0.6167123321626623,
0.7197683806448361,
0.5997967326505592,
0.4075235669728434,
0.4887068910619361,
0.40752356741334883,
0.30129716412690977,
0.3008288294546174,
0.30523019251416755,
0.22631691627651485,
0.06348012633018212,
0.008522867532059029,
0.0,
6.231884483462697E-8,
0.1203009802906692,
0.24237060662641652,
0.3403461841435844,
0.5082402830494543,
0.5029921938263724,
0.5268779617796129,
0.48939748566412733,
0.8393653237333767,
0.8238622211313831,
0.9039987761537025,
1.015035739105833,
0.6959056819853555,
0.9590572540240754,
0.8607860222763021,
1.0393475107774823,
0.7686742999541982,
0.997382663750982,
1.017227103561727,
0.6818330056406683,
0.9204157945238307,
0.6552106313267005,
0.7839330697606872,
0.5867316388908614,
0.7839330503005124,
0.8042061720157382,
0.6862743800309188,
0.7160406014035329,
0.8435003354145344,
0.6207434290737269,
0.7510722209716654,
0.5397377273037685,
0.4859077714639775,
0.4386027453138224,
0.48745786681863645,
0.4194756514346232,
0.3008289294749266,
0.3221490715994123,
0.3656776822517722,
0.3012971549143212,
0.21267801793198826,
0.08314318707697019,
0.05105853157462231,
0.0,
4.854910125450164E-8,
1.2266221314216018E-7,
5.8774343272996874E-8,
2.538548150142881E-7,
0.10772055376135953,
0.18851060131905117,
0.3931279845310225,
0.45089834568350395,
0.4682947263824626,
0.4893975205925661,
0.6252115495801959,
0.6684834730918665,
0.8663941784006159,
0.8849628290248804,
0.6252941257968392,
0.8335582913573886,
0.7426430224096006,
0.9444242593345367,
0.8220537253683813,
0.7623484052479212,
0.976662870779455,
0.7649875796176882,
0.8622145873725273,
1.0172271254447245,
0.7686743235707381,
0.9867446382118186,
0.4961792434287584,
0.7398586812635837,
0.541146769205241,
0.7341901841969041,
0.6226430440247748,
0.31723792921163646,
0.5778323564343021,
0.697030562258816,
0.6221505074582789,
0.20343143837325928,
0.7839330565285882,
0.8852129064301232,
0.8183705349693304,
0.6097790352134823,
0.6348635980920536,
0.3726210437662397,
0.5913769121965884,
0.47208389763878655,
0.22999220768542844,
0.42667279102220224,
0.3860967569962649,
0.450600411151323,
0.38293161144215515,
0.30129724523167073,
0.33182517843253395,
0.30129724023896487,
0.3318252125639489,
0.30082891234720477,
0.25845841707960443,
0.1709716534639892,
0.19418091637207696,
0.05105861171988739,
0.008509808635133991,
0.0033282958318596374,
7.462653977718288E-8,
0.0,
2.738801095402685E-9,
0.0,
4.424184781803563E-8,
0.0,
6.805928333307015E-8,
1.7058563098287318E-7,
0.07711818489433887,
0.11996146983234636,
0.2318599632107988,
0.31267723897352523,
0.3213771922407578,
0.44503211829394673,
0.2268805828810701,
0.45916106514113353,
0.5268780120302264,
0.4122963097627768,
0.16605266373597527,
0.7772139156648361,
0.5396168560444021,
0.570662649462157,
0.8379073496100284,
0.9444242450532752,
0.6959057705855909,
0.8342690105600306,
0.5883370322651307,
1.0314299927072494,
0.7724289567445162,
0.9973827073679882,
0.8622146119939932,
0.8572923045430607,
0.47786565131177955,
0.6668438568925218,
0.45274522343237567,
0.0,
0.2874830233625612,
0.12743054627507872,
0.0,
1.442376425939796E-7,
0.20404008685809114,
0.6127282924047284,
0.5438979789973857,
0.5997283237860668,
0.336581983237672,
0.2773646000945396,
0.38609676556251643,
0.40350442860516444,
0.4031248700346885,
0.4336289487206647,
0.30082900638363,
0.36836926305171197,
0.30082900176113575,
0.3221491080335108,
0.2791860301815794,
0.25801147421862114,
0.1485736487282067,
0.060826818969528226,
0.009723995546649569,
0.0,
6.847936802375564E-9,
0.0,
0.0,
9.945195033521113E-8,
1.156596615156043E-7,
1.0865995958343713E-7,
5.0688090709005414E-8,
0.0,
0.021402845300731638,
0.1823468117598111,
0.21826998237414183,
0.23916378710137914,
0.36868406711578083,
0.2248038638195537,
0.2722894906247425,
0.3615900533866284,
0.2829478626762042,
0.03431524358049665,
0.3262848620806152,
0.7382940509743667,
0.5246175206592752,
0.7285751347690199,
0.800267698627173,
0.8459999881991171,
0.38352739523604373,
1.0172271516432072,
0.8313546567178247,
0.7649876208184978,
0.5344823515573951,
0.510726522887381,
0.6026457864766013,
0.6668438792555549,
0.49617926777132093,
0.32671668282461885,
0.12743072861981258,
0.13558627262787848,
0.1274307899734488,
5.139181780729961E-8,
2.221246174589064E-7,
4.274816835831228E-8,
0.0,
0.0,
0.0,
0.4579073022695706,
0.3153816064084455,
0.3726210633158237,
0.28172181519694994,
0.38164877049716067,
0.2712247332048583,
0.35970179264612023,
0.28352691541612207,
0.22999227420773305,
0.27644630320492974,
0.28633513934719135,
0.2936257966771056,
0.30129725899440246,
0.26922399752467085,
0.2354539697942502,
0.17182973155187836,
0.18797706988181517,
0.10521119029665077,
0.027849826747908344,
0.005691207441414533,
0.008509837221768657,
3.347559401162786E-4,
6.694063128146907E-4,
5.330611859037722E-8,
8.09525818145868E-8,
0.0,
8.689673318223514E-9,
7.301223390405328E-9,
2.5731119112130124E-9,
0.0,
8.944234817855029E-8,
1.1143563371932276E-7,
1.1960852545435728E-7,
4.2809862828003604E-8,
0.057075283706655364,
0.09430993469693325,
0.21797010700333447,
0.21539909943384097,
0.3226501227504773,
0.24938280838258503,
0.22688060110097424,
0.0,
0.06803680992293408,
0.022430741130202582,
0.05610450007394509,
0.14016442452179775,
0.16178976066080616,
0.18973093308169828,
0.14865358513134386,
0.0,
0.436107713262272,
0.49123773730911624,
0.5586512421340433,
0.0,
0.70275444616408,
0.6378342462293883,
0.0,
0.0,
0.3757203882322053,
0.23339188598852878,
0.2798985433181714,
0.2966978376892097,
0.0,
0.0,
0.0,
0.0,
6.725583673666825E-8,
3.215592090719244E-8,
0.0,
0.0,
0.0,
0.0,
0.0,
0.1492760132829207,
0.0,
0.12295473099622602,
0.22059363168459778,
0.11619042894129422,
0.1812341391768019,
0.10230740367127518,
0.1327831842344795,
0.14249016502199743,
0.1435516094123961,
0.1304183233354329,
0.1088971308131238,
0.06971583914728868,
0.10296269292792362,
0.052043511404033724,
0.03225036247720848,
0.005028632832869197,
0.0,
8.381370531027735E-5,
4.610404845929077E-8,
0.0,
4.3122994084911996E-8,
0.0,
6.752221496797098E-8,
6.316964945884106E-8,
1.0266392532997435E-7,
0.0,
9.418514942490752E-8,
0.0,
1.213644291992675E-7,
0.012230279569083636,
0.026635187547967443,
0.1047373827320769,
0.08003427150876934,
0.13620415240941228,
0.09639690443969172,
0.0,
0.0,
0.020561632665908467,
0.05981544928625203,
0.0,
0.0,
0.08788027039118808,
0.0,
0.07844180376365086,
0.10000000000012364,
9.788795760118465,
10.867523783386195,
10.440007171734262,
9.319016830898674,
0.037025340399884824
], 'double')

def img_plot(obj):
    xs = []
    ys = []
    for sys in obj.systems:
        for img in sys.images:
            xs.append(img.pos.real)
            ys.append(img.pos.imag)
    scatter(xs, ys, 80, 'r')

def mass_plot(model):
    obj, data = model

    data['mass'] = XX[:489]
    R = obj.basis.maprad

    w,h,grid = obj.basis.mass_to_grid(data['mass'])

    x = linspace(-R,R, w)
    y = linspace(-R,R, h)
    X,Y = meshgrid(x,y)

    contour(X,Y,grid, 50, extent=[-R,R,-R,R], extend='both')
    img_plot(obj)
    xlabel('arcsec')
    ylabel('arcsec')
    return grid

def arrival_plot(obj, model):
    #lnr = poten(obj.basis.ploc, obj.basis.cell_size)
    s = obj.basis.array_offset + obj.basis.pix_start
    e = obj.basis.array_offset + obj.basis.pix_end

    L = obj.basis.L
    gx = linspace(-L,L, (2*L+1)*5)
    gy = atleast_2d(linspace(-L,L, (2*L+1)*5)).T

    lnr = poten2d(gx, gy, obj.basis.cell_size)

    print lnr, lnr.shape

    grid = zeros((2*L+1, 2*L+1))
    for y in xrange(2*L+1):
        for x in xrange(2*L+1):
            grid[y,x] = sum(model['mass'] * lnr)

    #print grid
    contour(grid)
    #gca().invert_yaxis()
    show()

    return grid


def potential_plot(model):
    obj, data = model

    lnr = obj.lnr

    print lnr, lnr.shape

    mass = data['mass']
    a = repeat(mass, repeat(5, mass.size)).reshape

    grid = zeros((2*L+1, 2*L+1))
    for y in xrange(2*L+1):
        for x in xrange(2*L+1):
            grid[y,x] = sum(model['mass'] * lnr)

    #print grid
    contour(grid)
    #gca().invert_yaxis()
    show()

    return grid
