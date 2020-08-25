# -*- encoding: utf8 -*-
import 	datetime
import 	imaplib
import 	email
import 	html2text
import 	json

def print_pick(p):
	try:
		to_print 	=	'''-----------------------------------------------------------------------------------------------------------\nMATCH: {}	\nPICK: {}	\t 	MARKET: {} - BET: {} \nStake: {}  	Odds: {} \t isLive: {} \t Tipster: {}\n-----------------------------------------------------------------------------------------------------------'''.format(p['match'], p['pick'], p['market'], p['bet'], p['stake'], p['odds'], p['isLive'], p['tipster'])
		print(to_print)
	except Exception as e:
		print('Could not print pick ({})'.format(e))


def get_market_from_pick(pick_):
	separators  = [' v ', ' - ', ' vs ', ' @ ']
	#	Obtenemos los equipos/jugadores participantes
	teams = []
	for sep in separators:
		if len(pick_['match'].split(sep)) == 2:
			for team in pick_['match'].split(sep):
				teams.append(team.strip())

	pick 	=	pick_['pick']
	
	for team in teams:
		try:
			if get_from_parenthesis(pick)[0] == team:
				return get_from_parenthesis(pick)[1]
		except:
			pass

	for it in get_from_parenthesis(pick):
		for t in teams:
			if t in it:
				return it.replace(t, '').replace('-','').strip()

	if 'Goalscorers' in get_from_parenthesis(pick):
		return 'Goalscorers'


	nba_markets 	=	[
		'Player Points And Rebounds',
		'Player Points And Assists',
		'Player Points',
		'Player Points, Assists And Rebounds',
		'Player Assists And Rebounds',
		'Player Assists',
		'Player Blocks',
		"Player Three's Made",
		'Winning Margin 3 Way',
		'Player Double Double',
	]


	if ' NBA' in pick_['pick']:
		print('NBA')


	for par in get_from_parenthesis(pick):
		if not par.replace('-','').isnumeric():
			return par


def set_market_and_bet(pick_):
	#	Recibe un objeto pick sin el market ni el bet. Devuelve el mismo objeto pick,
	#	pero con su market y bet ajustados en función del pick, el match, etc.
	#	Relación nombre del market:tipo de market para llamar a la función de bet
	markets_dict		=	{
		'Half Time Result':'result',	
		'Full Time Result':'participant',
		'Fulltime Result':'participant',
		'Half Time Result':'participant', 
		'Extra Time Result':'participant', 
		'Match Winner 2-Way':'participant',
		'Draw No Bet':'participant', 
		'Match Winner':'participant', 
		'Match Result':'participant', 
		'First Set Winner':'participant', 
		'To Win Match':'participant', 
		'Money Line':'participant', 
		'Team to Score in 2nd Half':'participant', 
		'Last Team to Score':'participant', 
		'Last Team To Score':'participant', 
		'Set 1 Winner':'participant', 
		'Set 2 Winner':'participant', 
		'Set 3 Winner':'participant', 
		'Set 4 Winner':'participant', 
		'Set 5 Winner':'participant', 
		'Set 6 Winner':'participant', 
		'Set 7 Winner':'participant', 
		'To Qualify':'participant', 
		'1st Goal':'participant', 
		'2nd Goal':'participant', 
		'3rd Goal':'participant', 
		'4th Goal':'participant', 
		'5th Goal':'participant', 
		'6th Goal':'participant', 
		'7th Goal':'participant',	
		'8th Goal':'participant',	
		'9th Goal':'participant',	
		'10th Goal':'participant',	
		'11th Goal':'participant',	
		'12th Goal':'participant',	
		'Tie Winner':'participant',	
		'2nd Half Result':'participant',
		'Money Line 3 Way':'participant',
		'First Team To Score':'participant',#or No Goals
		'Corner Match Bet':'participant',
		'Last Corner':'participant',
		'To Win 2nd Half':'participant',
		'To Win 1st Half':'participant',
		'Most Corners':'participant',

		#	yes/no
		'Both Teams to Score':'yes_no',
		'Both Teams To Score':'yes_no',
		'All sets played and 6-6 reached in final set':'yes_no',

		#	over/under
		'Match Goals':'over_under', 
		'Alternative Total Goals':'over_under', 
		'Alternative Match Goals':'over_under', 
		'Match Corners':'over_under', 
		'First Half Goals':'over_under', 
		'Goal Line':'over_under', 
		'Goals Over/Under':'over_under', 
		'Extra Time Goal Line':'over_under',
		'Alternative Goal Line':'over_under', 
		'Alternative Game Total 2':'over_under', 
		'1st Half Goal Line':'over_under', 
		'2nd Half Goal Line':'over_under', 
		'Extra Time Goal Line':'over_under', 
		'Goals Over Under':'over_under', 
		'Total Games in Set':'over_under', 
		'Total Games in Match':'over_under', 
		'Total Coners':'over_under', 
		'Asian Corners':'over_under',
		'1st Half Asian Corners':'over_under',
		'Game Totals':'over_under',
		'Total 2-Way':'over_under',
		'Total 2 Way':'over_under',
		'Goals Over Under':'over_under',
		'Corners 2 Way':'over_under',
		'Corners 2-Way':'over_under',
		'Corners':'over_under',
		'Total Points':'over_under',
		'2-Way Corners':'over_under',
		#'Total Corners':'over_under',
		'Total Corners':'over_under',
		'1st Half Totals 3 Way':'over_under',
		'Total Games in Set 1':'over_under',
		'Total Games in Set 2':'over_under',
		'Total Games in Set 3':'over_under',
		'Total Games in Set 4':'over_under',
		'Total Games in Set 5':'over_under',
		'Total Games in Set 6':'over_under',
		'Total Games in Set 7':'over_under',
		'Asian Goal Line':'over_under',
		'Team Totals':'over_under',
		'Number of Cards':'over_under',
		'Asian Total Corners':'over_under',
		'Asian Total Cards':'over_under',	# puede ser que haya que pinchar antes en tarjetas (navbar superior)	
		'Result Total Goals':'over_under',

		#	asian
		'Asian Handicap':'asian', 
		'Alternative Asian Handicap':'asian',
		'First Half Asian Handicap':'asian',
		'1st Half Asian Handicap':'asian',
		'Alternative Handicap Result':'asian', 
		'Alternative Handicap Result':'asian', 
		'3-Way Handicap':'asian', 
		'Handicap 2-Way':'asian', 
		'Handicap 2 Way':'asian', 
		'Handicap':'asian', 
		'Asian Handicap Corners':'asian',
		'Spread':'asian', 
		'Point Spread':'asian', 
		'Alternative Point Spread':'asian', 
		'Alternative 1st Half Point Spread':'asian', 
		'Match Handicap Sets':'asian',
		'Corner Handicap':'asian',
		'Puck Line':'asian',
		'Match Handicap':'asian',
		'Set 1 Handicap':'asian',  
		'Set 2 Handicap':'asian',  
		'Set 3 Handicap':'asian',  
		'Set 4 Handicap':'asian',  
		'Set 5 Handicap':'asian',  
		'Alternative Puck Line 2 Way':'asian',
		'1st Half Asian Handicap':'asian',
		'2nd Half Asian Handicap':'asian',
		'1st Half - Handicap':'asian',
		'2nd Half - Handicap':'asian',
		'1st Quarter Point Spread 3 Way':'asian',
		'2nd Quarter Point Spread 3 Way':'asian',
		'3rd Quarter Point Spread 3 Way':'asian',
		'4th Quarter Point Spread 3 Way':'asian',
		'1st Quarter Point Spread 2 Way':'asian',
		'2nd Quarter Point Spread 2 Way':'asian',
		'3rd Quarter Point Spread 2 Way':'asian',
		'4th Quarter Point Spread 2 Way':'asian',
		'1st Quarter Spread':'asian',
		'2nd Quarter Spread':'asian',
		'3rd Quarter Spread':'asian',
		'4th Quarter Spread':'asian',

		#	nba (13/11)
		'Player Points And Rebounds':'nba',
		'Player Points And Assists':'nba',
		'Player Points':'nba',
		'Player Points, Assists And Rebounds':'nba',
		'Player Assists And Rebounds':'nba',
		'Player Assists':'nba',
		'Player Blocks':'nba',
		"Player Three's Made":'nba',
		'Winning Margin 3 Way':'nba',
		'Player Double Double':'nba_player_yes_no',

		#	horse racing (13/11)
		'Win Only':'win_only',
		'Win only':'win_only',
		'E/W 3&1/4':'ew',
		'E/W 3&1/5':'ew',
		'E/W 4&1/4':'ew',
		'E/W 4&1/5':'ew',
		
		#	casos especiales
		'Double Result':'participant_participant',
		'Half Time Full Time':'participant_participant',
		'Teams To Score':'teams_to_score',
		'Match Result And Both Players To Win A Set':'mrabptwas',
		'1st Half Team Totals':'participant_over_under',
		'Result Total Goals':'participant_over_under',
		'Team Corners':'participant_over_under',
		'Goals':'participant_over_under',
		'Game Total':'participant_over_under',
		'First Team To Score':'participant_or_none',
		'Correct Score':'correct_score',
		'O/U':'o_u',
		'Corners Race':'corners_race',
		'Half Time/Full Time':'participant_participant',
		'Goalscorers':'player',
		'Time of 1st Goal':'ith_goal_time',
		'Goals Odd/Even':'odd_even',

		'Corners Race':'participant_value'

	}

	market 				= 	get_market_from_pick(pick_)
	market_types 		=	['participant', 'yes_no', 'over_under', 'asian', 'nba', 'win_only']

	if 	market 	in ['Game Lines', 'Match Lines', '1st Game', '2nd Game']:
		bet 	=	game_lines_bet(pick_)
	elif market in ['Double Chance', 'Half Time Double Chance']:
		bet 	= double_chance_bet(pick_['pick'], pick_['match'])
	elif market == 'Clean Sheet':
		bet 	= 	clean_sheet_bet(pick_['pick'], pick_['match'])
	elif markets_dict.get(market) == 'participant':
		bet 	= 	participant_bet(pick_['pick'], pick_['match'])
	elif markets_dict.get(market) == 'yes_no':
		bet 	=	yes_no_bet(pick_['pick'])
	elif markets_dict.get(market) == 'over_under':
		bet 	= 	over_under_bet(pick_['pick'],market)
	elif markets_dict.get(market) == 'asian':
		bet 	= 	asian_bet(pick_['pick'], pick_['match'])
	elif markets_dict.get(market) == 'win_only':
		bet 	=	win_only_bet(pick_['pick'])
	elif markets_dict.get(market) == 'ew':
		bet 	=	ew_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'nba':
		bet 	=	nba_bet(pick_['pick'])
	elif markets_dict.get(market) == 'double_result':
		bet 	=	double_result_bet(pick_['pick'])
	elif markets_dict.get(market) == 'teams_to_score':
		bet 	=	teams_to_score_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'mrabptwas':
		bet 	=	mrabptwas(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'participant_over_under':
		bet 	=	participant_over_under_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'participant_or_none':
		bet 	=	participant_or_none_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'participant_or_none':
		bet 	=	participant_or_none_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'correct_score':
		bet 	=	correct_score_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'o_u':
		bet 	=	o_u_bet(pick_['pick'])
	elif markets_dict.get(market) == 'nba_player_yes_no':
		bet 	=	nba_player_yes_no_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'corners_race':
		bet 	=	corners_race_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'participant_participant':
		bet 	=	participant_participant_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'player':
		bet 	=	player_bet(pick_['pick'])
	elif markets_dict.get(market) == 'ith_goal_time':
		bet 	=	ith_goal_time_bet(pick_['match'], pick_['pick'])
	elif markets_dict.get(market) == 'odd_even':
		bet 	=	goals_odd_even(pick_['pick'])
	elif markets_dict.get(market) == 'participant_value':
		bet 	=	participant_value_bet(pick_)
	else:
		bet 	=	''

	pick_['market'] 	=	market
	pick_['bet'] 		=	bet

	#	Devolvemos el objeto pick
	return pick_


#	Métodos para obtener el bet a partir de pick y market
def player_bet(pick):
	return pick[:pick.find('(')].strip()

def corners_race_bet(match, pick):
	#bet=[team/neither, number]
	bet = []
	separators  = [' v ', ' - ', ' vs ', ' @ ']
	team = ''
	for sep in separators:
		if len(match.split(sep)) == 2:
			for t in match.split(sep):
				if t in pick:
					team = t
				else:
					team = 'neither'
	bet.append(team)
	for n in pick.split():
		try:
			bet.append(float(n))
		except:
			pass
	return bet

def participant_participant_bet(match, pick):
	return pick[:pick.find('(')].strip()



def participant_value_bet(pick_): #Corners Race
	return[pick_['pick'].split(' - ')[1].replace('Race to ','').replace(' corners (Corners Race)','').strip(), pick_['pick'].split(' - ')[0].strip()]




def o_u_bet(pick):
	bet 	=	[]
	if 'Over' in pick:
		bet.append(pick[:pick.find('Over')].strip())
		bet.append('Over')
		bet.append(pick[pick.find('Over')+4:pick.find('(O/U)')].strip())
	elif 'Under' in pick:
		bet.append(pick[:pick.find('Under')].strip())
		bet.append('Over')
		bet.append(pick[pick.find('Under')+5:pick.find('(O/U)')].strip())
	return bet


def correct_score_bet(match, pick):
	#	Se supone que los dos únicos separadores serán ' v ' y ' @ '
	separators = [' v ', ' - ', ' vs ', ' @ ']
	#	Participant
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team.strip() in pick:
					bet = pick[pick.find(team.strip())+len(team.strip()):pick.find('(Cor')].strip()
					break
			break
	return bet

def participant_or_none_bet(match, pick):
	bet = ''
	separators = [' v ', ' - ', ' vs ']

	#	Participant
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team.strip() in pick:
					return team.strip()
	if not bet:
		return 'No Goals'




def participant_over_under_bet(match, pick):
	#	bet = participant + over/under + value
	pick = pick[:pick.find('(')]
	bet = []
	separators = [' v ', ' - ', ' vs ']

	#	Participant
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team.strip() in pick:
					bet.append(team.strip()) 
					break
			break

	#	over/under
	if ' Over ' in pick or ' over ' in pick or ' O ':
		bet.append('Over')
	else:
		bet.append('Under')

	#	value
	for it in pick.split():
		try:
			bet.append(str(float(it)))
		except:
			pass

	return bet

def goals_odd_even(pick):
	#	el pick tiene la forma: Even (Goals Odd/Even)
	return pick[0:pick.find('(')].strip()


def mrabptwas_bet(match,pick):
	#	match result and both players to win a set
	return [pick[:pick.find('(Ma')].split('&')[0].strip(), pick[:pick.find('(Ma')].split('&')[1].strip()]

def teams_to_score_bet(match, pick):
	# bet será un participant o 'both'
	separators = [' v ', ' - ', ' vs ']
	if 'Both Teams' in pick:
		return 'Both'

	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team.strip() in pick:
					bet = team.strip()
					break
			break
	return bet

def ith_goal_time_bet(match, pick):
	#bet = [team, ith, before/after, min]
	bet = []
	separators  = [' v ', ' - ', ' vs ', ' @ ']
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team in pick:
					bet.append(team)

	for ith in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th']:
		if ith in pick:
			bet.append(ith)

	if 'before' in pick or 'Before' in pick:
		bet.append('before')
	else:
		bet.append('after')

	for it in pick.split():
		try:
			bet.append(str(float(it.replace(':','.'))))
		except:
			pass

	return bet

def nba_bet(pick):
	player 	= 	''
	team 	=	''
	o_u 	=	'over'
	val  	= 	''
	team 	=	get_from_parenthesis(pick)[0]
	player 	=	pick[:pick.find(team)-1].strip()
	if ' under ' in pick or 'Under ' in pick:
		o_u 	=	'under'

	val 	=	pick[pick.find(o_u[1:])+len(o_u):pick.find(get_from_parenthesis(pick)[1])-1].strip()
	return [player, team, o_u, val]

def nba_player_yes_no_bet(match, pick):
	#	bet = [player, team, yes/no]
	bet = []
	separators = [' - ', ' vs ', ' v ', ' @ ']
	bet.append(pick[:pick.find('(')].strip())
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team in pick:
					bet.append(team)
	yes_no = 'no'
	if ' Yes' in pick or ' yes' in pick:
		yes_no = 'yes'
	bet.append(yes_no)

	return bet


def win_only_bet(pick):
	return pick[:pick.find('(Win')].strip()

def ew_bet(match, pick):
	return pick[:pick.find('(E/W')].strip()


def result_bet(pick):	
	bet 	= 	get_from_parenthesis(pick)[1]  	#	En este caso, bet es un resultado
	return bet

def participant_bet(pick, match):
	separators 	= 	[' - ', ' v ', ' vs ', ' @ ']
	bet 		=	''		#	En este caso, bet es un participant
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team.strip() in pick:
					bet = team.strip()
					break
			break
	#	Lo anterior funcionará para la mayoría de los casos. A veces, el pick no es el nombre de un equipo, sino 1, X ó 2 o la palabra 'Draw'
	if not bet:
		if 'Draw ' in pick:
			bet 	= 	'Draw'
		elif pick[0] in ['1', 'X', '2']:
			# caso gana local
			if pick[0] == '1':
				for sep in separators:
					if len(match.split(sep)) == 2:
						bet 	= 	match.split(sep)[0]
			elif pick[0] == '2':
				for sep in separators:
					if len(match.split(sep)) == 2:
						bet = match.split(sep)[1]
			elif pick[0] == 'X':
				bet 	= 	'Draw'
	return bet

def yes_no_bet(pick):
	bet 	= 	''	#	Para apuestas de sí o no (de momento sólo Both Teams to Score)
	for option in ['Yes', 'No', 'yes', 'no']:
		if option in pick:
			bet =	option.capitalize()
			break
	return bet

def over_under_bet(pick, market):
	bet 	=	[] 	
	pick 	=	pick[:pick.find('({}'.format(market))]
	pick 	=	pick[pick.find(')')+1:]

	if 'Over ' in pick or ' over ' in pick or 'over ' in pick:
		bet.append('Over')
	elif 'Under ' in pick or ' under ' in pick or 'under ' in pick:
		bet.append('Under')

	for sp in pick.split(' '):
		try:
			bet.append(str(float(sp)))
		except:
			pass
	return bet

def asian_bet(pick, match):
	separators 	= 	[' v ', ' - ', ' vs ', ' @ ']
	bet 		=	[]
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team in pick:
					pick = pick[pick.find(team):]
					bet.append(team)
					bet.append(pick[pick.find(team)+len(team):pick.find('(')].strip())
					break
			break
	return bet

def double_chance_bet(pick, match):
	separators 	= 	[' v ', ' - ', ' vs ', ' @ ']
	bet 		=	[]
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team in pick:
					bet.append(team.strip())

	if isinstance(bet, list) and len(bet) == 2:
		bet 	=	'{} or {}'.format(bet[0], bet[1])
		return bet

	if bet and len(bet) == 1:
		bet 	=	str(bet[0])
				
	if not bet:
		if '1X' in pick:
			for sep in separators:
				if len(match.split(sep)) == 2:
					bet = match.split(sep)[0]
					break

		elif 'X2' in pick:
			for sep in separators:
				if len(match.split(sep)) == 2:
					bet = match.split(sep)[1]
					break
					
		elif '12' in pick:
			for sep in separators:
				if len(match.split(sep)) == 2:
					bet = match.split(sep)
					break

	return bet



def clean_sheet_bet(pick, match):
	separators 	= 	[' v ', ' - ', ' vs ', ' @ ']
	bet 	=	[]
	for sep in separators:
		if len(match.split(sep)) == 2:
			for team in match.split(sep):
				if team in pick:
					pick = pick[pick.find(team):]
					bet.append(team)
					if ' Yes ' in pick or ' yes ' in pick:
						bet.append('yes')
					else:
						bet.append('no')
					break
			break
	return bet



def game_lines_bet(pick_):
	#	ej: bet = [participant, 'To Win']
	bet 	=	[]
	
	for part in get_participants(pick_):
		if part in pick_['pick']:
			bet.append(part)
			break

	#bet_ 	=	pick_['pick'].split(bet[0])[1].strip()
	
	bet.append(pick_['pick'].split(bet[0])[1].strip()[:pick_['pick'].split(bet[0])[1].strip().find('(')].strip())


	#bet.append(pick_['pick'][pick_['pick'].find(bet[0])+len([bet[0]]):].strip())
	
	return bet




#	Mátodos auxiliares
def get_participants(pick_):
	separators  = 	[' v ', ' - ', ' vs ', ' @ ']
	#	Obtenemos los equipos/jugadores participantes
	participants 	= 	[]
	for sep in separators:
		if len(pick_['match'].split(sep)) == 2:
			for part in pick_['match'].split(sep):
				participants.append(part.strip())	
			break

	return participants


def get_from_parenthesis(string):
	#	Recibe una cadena y devuelve los distintos elementos que hay entre paréntesis
	elements 	= 	[]

	while string.find('(') != -1:
		try:
			elem 	= 	string[string.index('(')+1:string.index(')')]
			#	paréntesis anidado
			if elem.find('(') != -1:
				elem 	=	elem[0:elem.index('(')].strip() #	con esta línea eliminamos el parénteis anidado.
				#elem 	= 	string[string.index('(')+1:string.index(')')+1] #	con esta línea incluímos en el elemento el paréntesis anidado.
				elements.append(elem)
				string 	= 	string[string.index(')')+2:]
			else:
				elements.append(elem)
				string 	= 	string[string.index(')')+1:]
		except:
			pass
	#	Funciona, pero no tiene en cuenta los elementos entre paréntesis anidados.
	#	Una opción sería eliminar los paréntesis anidados. Eso nos ayudaría, por ejemplo, 
	#	con los handicap asiáticos en live.
	return elements
