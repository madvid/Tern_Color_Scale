def tricolor_map(val1 = 0.0, val2 = 0.0, val3 = 0.0, mode=base):
	"""
	__Description__:
	
	"""
	
	if mode == base:
		return (min(val2+val3,1.0),min(val1+val3,1.0),min(val1+val2,1.0))
	if mode == 'RGB':
		return (val1, val2 , val3)
	if mode == 'RGB_2':
		return (val1**(1/2), val2**(1/2), val3**(1/2))
	if mode == 'RGB_3':
		return (val1**(2), val2**(2), val3**(2))
	if mode == 'RGB_4':
		return (val1**(1/3), val2**(1/3), val3**(1/3))
	if mode == 'RGB_5':
		return (val1**(1-val1), val2**(1-val2), val3**(1-val3))
	if mode == 'RGB_6':
		return (val1**(val1+val2), val2**(val2+val3), val3**(val3+val1))
	if mode == 'RGB_7':
		return (val1**(val1+0.5*(val2+val3)), val2**(val2+0.5*(val1+val3)), val3**(val3+0.5*(val1+val2)))
	if mode == "RGB_test":
		v1 = array([0., 1.])
		v2 = array([-sqrt(3)/2., -0.5])
		v3 = array([sqrt(3)/2, -0.5])
		normv_v1 = norm(v1)
		normv_v2 = norm(v2)
		normv_v3 = norm(v3)
		coord = val1 * v1 + val2 * v2 + val3 * v3 
		proj_nv1 = dot(coord, v1)
		proj_nv2 = dot(coord, v2)
		proj_nv3 = dot(coord, v3)
		res_1 = norm(proj_nv1 / normv_v1)
		res_2 = norm(proj_nv2 / normv_v2)
		res_3 = norm(proj_nv3 / normv_v3)
		return(min(res_1,1), min(res_2,1), min(res_3,1))
	if mode == 'sRGB':
		a = 1.055
		b = -0.055
		c = 12.92
		d = 0.0031308
		gamma = 1/2.4
		if val1 < d:
			f_r = c * val1
		else:
			f_r = a * (val1 ** gamma) + b
		if val2 < d:
			f_g = c * val2
		else:
			f_g = a * (val2 ** gamma) + b
		if val3 < d:
			f_b = c * val3
		else:
			f_b = a * (val3 ** gamma) + b
		return (f_r, f_g , f_b)
	if mode == 'AdobeRGB':
		gamma = 1 / 2.19921875
		f_r = val1 ** gamma
		f_g = val2 ** gamma
		f_b = val3 ** gamma
		return (f_r, f_g , f_b)

 

def plot_legend(colors, labels_txt, mode):
	"""
	__Description__:
	  Permet de générer un triangle de couleur avec graduation servant
	  d'échelle de couleur à 3 couleurs.
	  
	__Parametres__:
	  colors: [dict] dictionnaire à 3 clefs: "color_left", "color_right"
	  et "color_top". Les valeurs associées aux clefs doivent être gérées
	  par la librairie Matplotlib/Seaborn/Plotly
	  labels_text: [dict] dictionnaire à 3 clefs "label_left", "label_right"
	  et "label_top". Les valeurs associées aux clefs doivent être des str.
	"""
	# Check (moins que le minimum syndical mais mieux que rien)
	if not (isinstance(colors, dict) or isinstance(labels_txt, dict)):
		expt_msg = "colors et/ou labels_txt n'est pas un dictionnaire"
		raise Exception(expt_msg)
	for key in colors.keys():
		if key not in ["color_left", "color_right", "color_top"]:
			expt_msg = "Clef(s) de colors invalide."
			raise Exception(expt_msg)
	for key in labels_txt.keys():
		if key not in ["label_left", "label_right", "label_top"]:
			expt_msg = "Clef(s) de labels_txt invalide."
			raise Exception(expt_msg)

 
	# Vérification de l'existence de "tricolore.png"
	if path.isfile('tricolor_scale.png'):
		print("tricolore.png existe déjà.")
		return
	
	# Base de vecteurs pour le triangle
	P1 = [0.0, 1.0]
	P2 = [-sqrt(3) / 2, -0.5]
	P3 = [sqrt(3) / 2, -0.5]
	basis = array([P1, P2, P3])

 
	fig = plt.figure()
	ax = fig.add_subplot(111,aspect='equal')

 
	# Creation de la grille de points
	a, b, c = mgrid[0.0 : 1.0 : 50j, 0.0 : 1.0 : 50j, 0.0 : 1.0 : 50j]
	a, b, c = a.flatten(), b.flatten(), c.flatten()

 
	mesh = dstack((a, b, c))[0]
	mesh = list(map(lambda x: x / sum(x), mesh))
	mesh[0] = array((0, 0, 0))
	
	data = dot(mesh, basis)
	colours = [tricolor_map(pt[0], pt[1], pt[2], mode) for pt in mesh]

 
	ax.scatter(data[:,0], data[:,1],
			   marker=',',edgecolors='none',facecolors=colours)

 
	# Traçage du triangle et des lignes d'isovaleurs
	# contour extérieur noir:
	t0=plt.Polygon(basis[:,:], fill=False, ec="black", lw=2.5)
	
	disp1 = 2 * array([[0.1 * sqrt(3), 0.0], [0.1 * sqrt(3), 0.0]])
	disp2 = 2 * array([[0.0, 0.15], [0.0, 0.15]])
	disp3 = 2 * array([[-0.1 * sqrt(3), 0.0], [-0.1 * sqrt(3), 0.0]])
	
	r1 = [array([[-0.05 * dx * sqrt(3), -0.15 * dx], [0.0, 0.0]])
		  for dx in range(2, 12, 2)]
	r2 = [array([[0.05 * dx * sqrt(3), 0.0], [-0.05 * dx * sqrt(3), 0.0]])
		  for dx in range(2, 12, 2)]
	r3 = [array([[0.0, 0.0], [0.05 * dx * sqrt(3), -0.15 * dx]])
		  for dx in range(2, 12, 2)]
	
	t1 = [plt.Polygon(basis[:2] + r1[0] + disp1,
					  fill=False, ec="white", lw=1, ls=':')]
	t2 = [plt.Polygon(basis[1:] + r2[0] + disp2,
					  fill=False, ec="white", lw=1, ls=':')]
	t3 = [plt.Polygon(basis[[-1,0]] + r3[0] + disp3,
					  fill=False, ec="white", lw=1, ls=':')]
	
	# lignes blanches d'isovaleurs (quadrillage du repère)
	for i in range(1, len(r1)):
		t1.append(plt.Polygon(basis[:2] + r1[i - 1] + i * disp1,
							  fill=False, ec="white", lw=0.6, ls='-'))
		t2.append(plt.Polygon(basis[1:] + r2[i - 1] + i * disp2,
							  fill=False, ec="white", lw=0.6, ls='-'))
		t3.append(plt.Polygon(basis[[-1,0]] + r3[i-1] + i * disp3,
							  fill=False, ec="white", lw=0.6, ls='-'))
	
	plt.gca().add_patch(t0)
	for t in t1:
		plt.gca().add_patch(t)
	
	for t in t2:
		plt.gca().add_patch(t)
	
	for t in t3:
		plt.gca().add_patch(t)
	
	# Affichage et position des labels
	offset = 0.25
	fontsize = 28
	xy_lbl_int = (array(P1) + array(P3)) / 2 + offset * array([2, 0])
	xy_lbl_ext = (array(P1) + array(P2)) / 2 - offset * array([2, 0])
	xy_lbl_tech = (array(P3) + array(P2)) / 2 - offset * array([0, 1.15])
	ax.text(xy_lbl_int[0], xy_lbl_int[1],
			'$legend_1$', horizontalalignment='center', verticalalignment='center',
			fontsize=fontsize, rotation = -60)
	ax.text(xy_lbl_ext[0], xy_lbl_ext[1], '$legend_2$',
			horizontalalignment='center', verticalalignment='center',
			fontsize=fontsize, rotation = 60)
	ax.text(xy_lbl_tech[0], xy_lbl_tech[1],
			'$legend_3$', horizontalalignment='center', verticalalignment='center',
			fontsize=fontsize)
	
	# Génération des valeurs pour les coordonnées suivant les différents axes
	v_ext_int=basis[0]-basis[1]
	v_int_tech=basis[2]-basis[0]
	v_tech_ext=basis[1]-basis[2]
	left_ascending_ticks = [[basis[1][0] + 0.2*i*v_ext_int[0],
							 basis[1][1] + 0.2*i*v_ext_int[1],
							f'${str(2*i/10)}$'] for i in range(1,5)]
	right_descending_ticks = [[basis[0][0] + 0.2*i*v_int_tech[0],
							 basis[0][1] + 0.2*i*v_int_tech[1],
							f'${str(2*i/10)}$'] for i in range(1,5)]
	bottom_ticks = [[basis[2][0] + 0.2*i*v_tech_ext[0],
					 basis[2][1] + 0.2*i*v_tech_ext[1],
					 f'${str(2*i/10)}$'] for i in range(1,5)]
	delta = -0.2
	for coord1, coord2, coord3 in zip(left_ascending_ticks, right_descending_ticks, bottom_ticks):
		ax.text(coord1[0]+delta, coord1[1], coord1[2], horizontalalignment='center',
			verticalalignment='center', fontsize=int(0.7*fontsize), rotation=-33)
		ax.text(coord2[0]-delta, coord2[1], coord2[2], horizontalalignment='center',
			verticalalignment='center', fontsize=int(0.7*fontsize), rotation=33)
		ax.text(coord3[0], coord3[1]+0.6*delta, coord3[2], horizontalalignment='center',
			verticalalignment='center', fontsize=int(0.7*fontsize))
	
	ax.set_frame_on(False)
	ax.set_xticks(())
	ax.set_yticks(())

 
	plt.savefig(fname="tricolor_scale.png")