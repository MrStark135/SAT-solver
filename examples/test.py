import solver

"""Tests the solver with two CNFs - SAT with one exact solution to check against, and UNSAT to check against None
"""

# SAT CNF that has a single solution - test w/truth_cnf_sat
cnf_sat = [
	['~CL', '~BW'], ['CG', '~BE'], ['V', '~CK', '~CF', '~CR'], ['U', 'BP', '~CL', '~BD', '~BU', 'CE', '~AY', 'T'], ['CP', '~BC', 'AT', 'L', 'BI', 'O'],
	['~W', '~BY'], ['AH', '~CJ'], ['~AZ', 'AP'], ['~J', 'H', 'BK', 'BZ', 'X', 'AP'], ['~AM', '~CF', '~H'],
	['~BF', '~AP'], ['~CV', '~CO', 'BG', 'BH', '~AP'], ['BJ', 'BV'], ['~CJ', 'CA'], ['AI', 'K', 'AR', 'AE', '~E', 'BJ'],
	['~BH', 'BQ', 'Z'], ['~CV', '~A', 'CD'], ['~AW', '~BD', '~AB', 'F', 'R', 'AO', '~BU', 'BT'], ['~CQ', '~BK', '~M', 'AT', 'B'], ['BU', '~CM'],
	['R', '~B'], ['Z', '~AV'], ['F', 'BG'], ['AG', '~CU'], ['~AY', '~BR'],
	['~C', 'BT', '~M'], ['BI', '~BD', '~BJ'], ['~F', 'AY'], ['CI', 'E'], ['BM', '~CA', 'AI', '~AK'],
	['~CP', '~BU'], ['~AP', '~Z'], ['BH', 'CB', '~Q', 'BO'], ['B', 'AC', '~CV'], ['B', 'CI', '~AA', '~AN', 'N', 'AU', '~V', '~P'],
	['BI', '~I', 'CC'], ['B', '~CN'], ['AF', 'O', '~CR'], ['~G', '~Q', 'CC', 'CG', '~D'], ['AO', '~O'],
	['~CB', '~AF'], ['CM', '~CJ'], ['D', '~C', '~AM'], ['~BU', '~CJ', 'BO', '~BC', '~CQ'], ['M', '~G'],
	['~CF', 'B', 'R', 'BX'], ['BT', '~H', '~BU', '~AW'], ['~CM', 'R', '~A'], ['~AN', '~BR', 'BD', '~BC'], ['AJ', '~J', '~CU', '~AT'],
	['V', '~BV', '~M', 'CR'], ['~CA', 'BD'], ['AK', 'BC', '~H', '~F', '~BI'], ['CT', '~AL'], ['~AS', '~CQ'],
	['BO', 'BI', 'BZ', 'CH'], ['AI', 'D'], ['~CQ', '~BS', '~BI', 'BE'], ['AA', '~L', '~CG'], ['~BR', 'AN', 'B'],
	['~BA', '~N'], ['AT', '~CM', 'A'], ['~BW', '~AZ'], ['AV', 'BK'], ['~R', '~AB'],
	['CT', 'AY', 'CB'], ['~D', 'AD'], ['~AS', 'CN', '~CG'], ['~CO', 'BP'], ['AL', 'BA'],
	['~BS', 'AB'], ['~P', 'AU'], ['~CL', 'BN', '~CR'], ['~CJ', '~E'], ['AP', '~BE'],
	['~BS', 'K', '~Q', 'AG'], ['~B', 'AR'], ['AF', 'D'], ['BO', 'AS'], ['BW', '~CR'],
	['~CE', 'CL', '~BX', 'BL', 'CT'], ['~AJ', 'BM'], ['CS', 'K'], ['B', 'BZ'], ['~AZ', '~W'],
	['AR', 'T', 'AF', 'AX', 'W'], ['~BT', 'BI', '~CM'], ['N', '~AE'], ['AP', '~BY', 'AV'], ['~BQ', 'AS'],
	['BE', 'AI', 'CK', '~CS', '~CF'], ['BB', '~CR', 'CJ', 'P', '~AE', 'AS'], ['C', 'AJ', '~BT', '~CG', 'AK', '~CJ'], ['~BU', '~CJ'], ['~AF', 'CS', 'BB'],
	['BN', 'AY', '~D'], ['~R', 'CI', 'W'], ['AD', '~BM', 'BY', '~N'], ['~AI', 'AT'], ['~O', 'BT', 'AY', '~AP', '~U'],
	['AG', '~CQ', 'AO'], ['~L', 'Y'], ['L', '~Z', '~BJ', 'BQ', 'V', 'D', '~CA', 'BG'], ['CD', '~AV', 'Q', '~G'], ['AW', 'BX'],
	['Y', 'AN', '~BY'], ['~AZ', '~CI', '~CS'], ['~AQ', 'AR'], ['~CD', '~O', 'R', '~AW'], ['~BO', 'BF'],
	['~AB', '~M', 'AU', '~BZ', '~BS', '~CL'], ['~AX', '~T'], ['CE', 'A'], ['AC', '~I', '~BR', 'AN', 'P'], ['B', 'CM', 'BA'],
	['Q', '~CH'], ['CM', '~AB', 'CK'], ['~CD', 'BH'], ['CA', 'CQ', '~BM', '~U'], ['~AO', 'BN'],
	['~T', 'B'], ['J', 'BL'], ['~AM', 'AQ', 'L', '~AN'], ['AG', 'CA'], ['AQ', 'X', '~AE'],
	['~B', 'BO'], ['~BU', 'BM', '~AW', '~BX', '~C', '~CK'], ['~H', '~BQ', 'K', '~BD'], ['CJ', '~X'], ['BY', '~U'],
	['CQ', 'CO', 'CL', '~N', 'BY', 'W', '~C'], ['AB', 'T'], ['AP', 'CN'], ['R', 'BO', 'BV', 'AZ'], ['~AG', 'CA'],
	['~BL', 'CB'], ['~BR', '~AQ', '~D'], ['~S', 'AG'], ['~AC', '~CT'], ['~AX', 'J', 'I', '~CM'],
	['CH', 'BH', 'BQ'], ['B', '~AT', '~CF', 'BW'], ['~AI', 'CL', 'AV', '~AT', '~N'], ['~BL', '~BO', 'BW', 'BN'], ['G', 'AC'],
	['B', '~AL', 'AE', '~BJ'], ['~BV', 'AV', '~CR', '~AL'], ['~CC', '~H'], ['BQ', '~X', '~C'], ['AT', 'AY', 'CL'],
	['~CV', '~BF', '~BU', '~AS', '~H', 'CH'], ['~AA', 'BK', '~G', 'AK', 'AT', 'AG'], ['CQ', '~BS'], ['W', 'BQ'], ['BZ', '~F'],
	['BQ', '~CF', 'CC', '~CQ'], ['BS', '~CE'], ['~BR', 'AV'], ['~AW', '~CA'], ['~BM', 'CL'],
	['~S', 'B'], ['~AT', 'CC'], ['~A', '~CS'], ['CH', 'L'], ['BS', 'AB', '~C'],
	['~BI', '~BG'], ['~CN', 'AY'], ['T', '~Z', '~BG', 'N'], ['U', 'CO'], ['AH', 'AO'],
	['~BM', 'D', '~CF', 'BB'], ['D', '~BT'], ['~I', '~CQ', '~AC'], ['~AG', '~BW', '~AO', '~AI', 'CO', '~CT', '~AS', '~G'], ['~Y', 'CP'],
	['U', 'AY'], ['V', 'S', 'BO', '~I'], ['~CJ', '~BR'], ['AZ', '~CU'], ['BE', '~AW'],
	['AS', 'I', 'AG'], ['CL', 'N'], ['AS', 'CF', '~BU', '~AA'], ['~U', 'BD', 'BK', '~CQ', 'R', 'A'], ['~AB', '~BG', '~J'],
	['~F', 'S'], ['K', '~BR', '~CJ'], ['BB', 'BI'], ['~CH', 'AR', '~A', 'CA', 'V'], ['AI', '~BJ', 'L', '~CD', '~CA', 'AJ', 'BP', 'AU'],
	['BI', '~CU', '~E'], ['BP', '~BQ', '~AY'], ['AC', 'D', '~BY'], ['AK', '~AY', 'J', '~H'], ['~CI', 'AF', '~E', 'AG', 'V', 'T'],
	['BJ', 'X', '~BY', 'CV', '~AV'], ['~W', 'BB', 'BM', '~BZ', 'Q', 'I', 'CS'], ['CT', '~CH', '~S'], ['BR', 'CK', 'CL', '~CS'], ['~R', '~AS', 'AZ', 'AM', '~CU', '~BY'],
	['~BR', 'CS', 'CM', 'BF', 'BO', '~AR', '~AL'], ['D', '~CL', 'CR'], ['~A', '~P', 'CD', '~K'], ['~CD', '~Y', 'BP', '~BM', 'T'], ['~BR', 'U', 'CI', 'E', '~BU'],
	['C', '~CG'], ['U', '~BJ', '~AI', '~BG', 'BT'], ['AE', 'A'], ['BK', 'AB', '~CU', 'AC', '~CM', '~AI'], ['~CU', 'BY', '~L', '~AF', '~BW'],
	['AE', 'AI'], ['CJ', '~BY', '~BU', 'BK'], ['AV', '~AM', '~H', 'AC', 'P', 'X', '~BZ'], ['AS', '~G'], ['~BC', '~BB'],
	['CG', '~CM', '~F', '~J', 'AZ', '~CL'], ['~CI', 'AI', '~AY'], ['~CK', '~AX'], ['~K', 'T', 'A', '~X', '~BP'], ['AN', '~BJ'],
	['H', 'V'], ['~BE', '~BK'], ['CU', '~CF'], ['~CI', '~BX', '~BI', 'CL', '~BZ', '~BR', '~AN'], ['~E', '~BY'],
	['~CL', '~BY', 'BD'], ['~BN', 'Y'], ['~I', 'BZ'], ['AB', 'E'], ['CV', '~C'],
	['M', 'CL', '~S', '~CU', '~BJ'], ['BC', '~Z', 'S'], ['BM', 'BI', 'CA'], ['~AR', 'BC'], ['~AK', '~AA'],
	['BF', '~BM'], ['~CA', '~AP'], ['~BK', '~O'], ['AU', '~BG', 'BX'], ['CN', '~AO', 'BJ', 'BF', '~CH', 'AT', 'CQ', '~BW'],
	['CR', 'AQ'], ['BG', '~Z'], ['~BZ', '~J'], ['~BG', 'AI'], ['BX', '~BR', 'AB', '~CE', 'D', '~BH'],
	['~AU', '~CV'], ['~BX', 'CS', 'CV', '~T', 'BM', 'CK'], ['CA', 'BN', '~N', 'X'], ['~K', 'I'], ['BA', 'R', 'BQ', '~X', '~AH', '~CK'],
	['O', 'X', '~AK', '~H'], ['AM', 'BQ'], ['CF', '~AM'], ['~E', 'CT', 'K', '~CI'], ['AA', 'CK'],
	['~BK', '~AP', 'L'], ['~BN', 'AJ'], ['AK', '~N', '~S'], ['~AZ', '~BG', 'F', '~BX', 'AS', '~CN', '~AV', 'CT'], ['~K', 'Y', 'CU', '~Z', '~BO'],
	['O', '~CI'], ['~AN', 'CV', '~AI'], ['CE', '~CD', '~D', '~CV', '~CG'], ['BJ', 'I', '~CB', 'AJ', 'AW', 'CO'], ['~BG', '~BN', '~AW', '~U'],
	['P', 'L', 'AC'], ['~BX', 'W'], ['F', 'AY'], ['~X', '~AD', '~O', '~AH', '~CS'], ['~H', 'AP', 'AK', '~W'],
	['BT', '~AZ'], ['BR', '~Q'], ['K', '~AU', 'BE'], ['~E', '~D', '~CR', 'AB', 'CA'], ['M', '~AJ', '~AH', '~AL'],
	['AX', '~M'], ['~AD', 'AK'], ['~BG', 'AX'], ['~BP', '~AN'], ['AM', 'K', '~BC'],
	['AG', '~AA', 'CA'], ['~V', '~AH'], ['~BH', '~BT'], ['~F', '~AO', 'BD', '~AN', 'R', 'G', '~BP'], ['V', '~CT', '~AO', '~R'],
	['~I', 'AK', '~CQ', 'BF'], ['A', '~Q', 'AE', '~BQ', 'CD', '~BU', 'AP', '~AQ'], ['F', '~CQ'], ['A', '~AW', '~O'], ['~AV', '~AH'],
	['~BD', 'P'], ['AH', '~CM'], ['~AB', 'H', '~CP', 'R'], ['~P', '~BM', 'V', 'BK', '~CI', 'AO'], ['~W', 'R'],
	['X', 'CD'], ['~BV', 'F'], ['BV', 'CB', 'AW', 'AT', 'V'], ['~AT', 'D', 'AC'], ['~G', 'CT', 'E', 'AL'],
]
truth_cnf_sat = {
	'A': True, 'B': True, 'C': False, 'D': True, 'E': True, 'F': True, 'G': False, 'H': False, 'I': True, 'J': False,
	'K': True, 'L': True, 'M': False, 'N': False, 'O': False, 'P': True, 'Q': False, 'R': True, 'S': True, 'T': True,
	'U': False, 'V': True, 'W': True, 'X': False, 'Y': True, 'Z': False, 'AA': False, 'AB': False, 'AC': True, 'AD': True,
	'AE': False, 'AF': False, 'AG': True, 'AH': False, 'AI': True, 'AJ': True, 'AK': True, 'AL': False, 'AM': False, 'AN': False,
	'AO': True, 'AP': False, 'AQ': True, 'AR': True, 'AS': True, 'AT': True, 'AU': True, 'AV': False, 'AW': False, 'AX': False,
	'AY': True, 'AZ': False, 'BA': True, 'BB': False, 'BC': True, 'BD': True, 'BE': False, 'BF': True, 'BG': False, 'BH': True,
	'BI': True, 'BJ': False, 'BK': True, 'BL': True, 'BM': True, 'BN': True, 'BO': True, 'BP': True, 'BQ': True, 'BR': False,
	'BS': False, 'BT': False, 'BU': False, 'BV': True, 'BW': False, 'BX': True, 'BY': False, 'BZ': True, 'CA': True, 'CB': True,
	'CC': True, 'CD': True, 'CE': False, 'CF': False, 'CG': False, 'CH': False, 'CI': False, 'CJ': False, 'CK': True, 'CL': True,
	'CM': False, 'CN': True, 'CO': True, 'CP': True, 'CQ': False, 'CR': False, 'CS': False, 'CT': False, 'CU': False, 'CV': False,
}

cnf_sat_small = [
	['A', 'B'],
	['~A', '~B'],
	['A']
]
truth_cnf_sat_small = {
	'A': True, 'B': False
}

# UNSAT CNF to test properly the solver for conflict detection
cnf_unsat = [
	['BC', '~BA'], ['~AY', 'BY', '~H', '~A'], ['AL', '~CR', '~AR', '~O'], ['AH', 'BQ', 'P', 'BG'], ['AF', '~AC'],
	['~BX', '~BS'], ['AR', 'D'], ['I', '~E'], ['~CB', 'BQ'], ['~BR', 'AC', '~CE'],
	['~I', '~AZ', '~BK'], ['AC', '~CD', '~Y'], ['C', '~CG', '~AY'], ['~AQ', 'CI', 'O', '~BB', '~BW', 'AN', '~CO', 'CK'], ['BA', '~BK'],
	['BQ', 'AR', '~BR', '~AT', 'CI', 'CU', '~CO', 'CJ'], ['~AK', 'BZ'], ['P', 'BH', 'CK'], ['CC', '~CE', 'F', '~AN'], ['~AD', '~AX'],
	['~CK', 'AM', '~D'], ['B', 'BV', 'AK'], ['F', '~AZ', 'G', 'BU', 'BT', '~Y', '~AU', '~BS'], ['BR', 'AR', '~CE', '~W', '~CV', 'CJ'], ['~CI', 'BR'],
	['~J', 'AL', '~M', 'BM', '~CU'], ['~BM', '~BZ', 'BD', 'M'], ['J', 'BF', '~W', 'CN', 'BE', '~L'], ['~CM', 'U', '~AN'], ['~CQ', 'BB', 'BP', 'O'],
	['~BY', '~BN', 'CR'], ['~CA', '~CQ', 'M'], ['AK', '~K', 'CT', '~U', '~AI'], ['~R', 'N'], ['CT', 'CS', 'W'],
	['~D', '~AU', '~BS', 'BV', 'AV', 'BH'], ['~N', 'AS', '~BT', 'AV'], ['AG', '~AB', 'T', '~BS', 'CP'], ['BE', 'AE', '~AU', 'M'], ['W', 'CQ'],
	['~CN', '~CM', '~CL', '~CD', '~W', 'AU'], ['~CQ', 'V'], ['AQ', 'BA', 'CK'], ['~CQ', 'AJ'], ['CS', '~AE'],
	['AC', '~R'], ['AA', 'CJ'], ['CF', 'T', 'J'], ['AF', 'CS'], ['~BP', '~AU', '~AY', '~AO', 'CF', 'AJ'],
	['CL', 'BG'], ['AE', 'CO'], ['A', 'AT'], ['~BL', '~AZ'], ['~AJ', 'F'],
	['AK', '~BC'], ['~CJ', 'AD', '~AH'], ['~AC', 'R'], ['~BE', '~CL', '~BK'], ['BU', 'F'],
	['J', 'H', 'V'], ['CN', 'AL', 'BN'], ['BV', 'AZ', '~CM', 'CD'], ['AE', 'AW', 'BV'], ['~BW', '~AH'],
	['CI', '~BY', 'G', '~CC', 'CE'], ['~BT', 'CT', 'BB'], ['BS', 'BP'], ['D', 'AX'], ['CT', 'BV'],
	['~AV', '~AN', '~CO', '~AP'], ['~AN', 'N'], ['~O', '~J'], ['AC', 'AI'], ['~AP', 'Y', '~CL'],
	['CH', '~B', '~BH'], ['~BZ', 'S', '~AO', 'CN', '~CP', 'AS', '~AZ'], ['R', 'BH'], ['~BT', 'AF'], ['~CV', '~BC'],
	['~AF', 'AC'], ['Y', '~BB'], ['BQ', 'BJ', 'AS'], ['AK', 'U'], ['~H', '~BN'],
	['AL', '~AT', '~AV'], ['~Q', '~BI'], ['BS', 'A'], ['~BN', '~BX', 'N', 'BF'], ['N', '~CI'],
	['~CS', 'CB', 'G', 'CI'], ['BD', 'W'], ['AF', '~BI'], ['~D', 'CQ'], ['~K', 'CA', '~AW'],
	['~AQ', '~AF', '~Q', '~BU'], ['~U', 'Z', 'BZ', '~R', '~AG'], ['BC', '~AO', 'CH', '~AG'], ['~AJ', 'AF'], ['CI', 'CO', '~AE', '~BE', 'CA'],
	['BP', 'BO', 'CA', 'U', 'AU'], ['~BG', '~CB'], ['D', '~CQ'], ['N', '~AF', 'BD', 'BX'], ['~CV', '~AS', '~CP', 'CE', '~S'],
	['~Q', 'CH', 'CL', '~CQ', 'CJ'], ['~T', '~BU', '~AM'], ['~CD', 'O'], ['~BR', '~K'], ['~A', '~J'],
	['CB', 'K'], ['~AC', '~O', 'BH'], ['CG', 'BW'], ['~W', 'Q', '~AW', 'BQ'], ['~S', '~BU', '~CG', '~AZ'],
	['~AG', '~CR', 'C', '~AT', '~I', 'AS'], ['~CG', 'N'], ['CH', 'N'], ['CU', 'AK', 'CM', '~AA', 'CK', 'BK', 'AO', '~BJ'], ['BD', 'O', '~AK', '~CI'],
	['BP', '~BA', 'CU', 'BV', 'J', '~Q'], ['~BG', '~AO'], ['~U', 'X', '~CK', 'CU', 'CB'], ['~N', 'CI'], ['~CA', 'CF'],
	['CQ', '~AJ'], ['~AK', 'AG', '~CO', '~CG', 'BZ'], ['CR', 'BS'], ['BY', '~AP'], ['~CN', '~Z'],
	['~AH', 'AY'], ['~BO', '~BF'], ['~BX', '~BU'], ['BG', 'AM', '~Z'], ['~L', '~CS'],
	['AZ', '~CP'], ['AR', '~X', 'BL', '~CK', 'AV', '~BO'], ['BR', 'AL', 'AP', 'N', '~K', 'CG'], ['AG', '~AP', 'O'], ['AJ', 'CB', 'CD', 'BW'],
	['BI', 'Y', 'AV', 'CI', 'BV'], ['CI', '~CO', 'AY', '~BT'], ['~BT', '~B'], ['CV', 'BA', 'F'], ['CR', 'BP', 'AB', '~AW'],
	['~BR', '~CD'], ['~CB', 'CK', 'AY'], ['V', '~U', 'AP', '~CM', 'AC', '~AS'], ['~BT', 'CT'], ['~C', '~CB'],
	['~AZ', 'CK'], ['I', 'BB'], ['~AF', 'BI'], ['BK', '~BZ', '~BE', 'BB'], ['~AF', 'Y'],
	['~BK', 'CA', '~BA', 'AJ'], ['T', 'BZ', 'BN', 'R', 'AP', 'CA', '~AO', 'U'], ['E', 'AD', '~AK'], ['~AS', 'I'], ['U', 'A', 'BA'],
	['~Z', '~S'], ['~N', 'CI', '~AD', '~BI'], ['AS', 'BF', '~F', '~CP', 'AT', 'CA'], ['AS', 'CE'], ['~CG', 'AV'],
	['BZ', '~CR', 'BL'], ['~S', 'CJ', 'AF', 'E', '~BV', 'CL', '~O', 'Y'], ['~AQ', 'AJ'], ['CC', 'BN', '~BV', 'AE', '~CN', 'S'], ['BF', 'AS', '~D', 'BB', '~G'],
	['R', '~N'], ['~AX', 'CG', '~CF'], ['BN', '~CG'], ['X', '~BW', 'BD'], ['~M', '~BP', 'BG'],
	['~BF', '~E', 'H', 'AV', '~AK'], ['AV', '~AC', '~D', '~AO', 'M'], ['~BS', 'AL', '~CL'], ['~AC', 'D'], ['CN', '~BE', '~J', '~K'],
	['~AV', 'BW'], ['~CE', 'BC'], ['~O', 'N'], ['CL', '~BO'], ['CQ', '~BE'],
	['CD', '~O'], ['~AG', 'G'], ['BY', 'BD'], ['~CV', 'BS', '~CD', '~BX', '~X', 'CU'], ['~AB', 'BR'],
	['AI', 'BF', '~AF', '~S', 'M', 'G', '~AL'], ['O', '~AU'], ['BA', 'G', 'Y'], ['P', '~G', '~AE', 'BB', '~CD'], ['O', '~AL'],
	['~BD', 'BZ'], ['AY', '~AV', '~AR', '~BT', '~AU', 'CS', 'S', 'Z'], ['~G', '~AK', 'BL', '~BY', 'CF', 'CI', 'BI', 'BQ'], ['~CT', 'U', 'BL', '~BN', '~BH', 'AN', '~C'], ['BM', '~BR', '~BL'],
	['~CG', '~K', '~U'], ['~AZ', 'H'], ['AD', 'BA', '~AR', 'BG'], ['AD', 'BH', 'CD'], ['CT', '~G', 'AA'],
	['~X', 'CH', 'K', '~BP', 'AU', 'I'], ['~E', '~BI'], ['BR', '~AU', 'BP', 'BM'], ['~CB', 'AO'], ['AE', '~CC', '~CJ'],
	['O', '~D'], ['BF', '~BV', '~CF', 'Y', '~AP'], ['Q', '~BM', 'BX'], ['CU', '~Q'], ['~AD', 'CI', '~BV'],
	['AR', 'CT'], ['AO', '~CC', '~CN'], ['~BS', '~M'], ['~CM', '~BD'], ['AZ', 'CH'],
	['~E', '~AM', '~BL', 'O'], ['~AZ', '~P'], ['Q', 'F'], ['~BT', 'P', 'AH', '~CV', '~CM', '~BF'], ['BD', '~AU'],
	['CE', 'D', '~H', 'BJ'], ['BN', 'AE'], ['AI', 'CL', '~CT', '~AN'], ['~AR', '~CN', '~K', 'BM', 'CE'], ['~X', 'BK'],
	['F', '~CE', 'CU', 'BV', 'AH', 'CF', '~AA'], ['BI', 'CL', '~R', '~CT', '~CM'], ['AP', 'AB'], ['~CB', '~CR'], ['~AU', 'BD'],
	['~BR', 'CS'], ['BE', 'AM', '~BX'], ['~AG', 'AD', '~P'], ['BG', '~AS'], ['E', 'AL', 'Z', '~F', '~AO', 'AN'],
	['~AN', '~CF', 'CL', 'CG', 'AY'], ['~AT', '~N', 'BV', '~BM'], ['~U', 'CL'], ['CQ', '~F', 'BD', 'C'], ['CH', '~P', 'BA', 'AT'],
	['~BP', '~BA', '~BU'], ['AN', '~X', '~AB', '~AR', '~CU'], ['H', '~G'], ['N', '~CL'], ['L', '~AL', '~AP', '~CR'],
	['~AH', 'CS'], ['~BR', '~AG', '~W', 'O'], ['AJ', '~AF'], ['~CT', '~AG', 'AL', 'AP'], ['C', 'AP', '~V', 'CB'],
	['~BE', 'CI'], ['~AD', 'AQ', '~CV', '~S'], ['AA', 'BD'], ['CI', '~BR'], ['CS', '~BB'],
	['A', 'AX'], ['AC', '~I'], ['~CR', '~BQ', '~CT'], ['BD', '~CQ', '~AP'], ['~BM', '~CV', 'CA', 'BI', 'CQ', 'CP', '~H', 'CM'],
	['CU', '~CV'], ['CJ', 'BU', '~CE', 'CD', '~CB'], ['~W', '~BZ', 'T', 'CT', 'CF'], ['BG', '~AV', 'CH', '~CR'], ['D', '~O'],
	['~O', 'D'], ['~CC', '~AM', '~CA', 'BQ', '~L', '~BM', '~CE'], ['AU', 'AX', 'BU', 'E', '~BZ', '~T'], ['~CR', '~AR', '~AC', '~AQ'], ['CT', '~BS', 'E'],
	['~AJ', '~Y', '~P', '~BG'], ['AH', '~AA'], ['Q', '~CG'], ['~BI', 'C'], ['X', 'G'],
	['~AT', 'CV', 'G', 'CF', 'AQ', 'AI'], ['~CP', '~BK'], ['BV', 'CI'], ['BH', 'CL'], ['BQ', '~AB'],
	['~F', '~AT'], ['C', '~L'], ['~CJ', 'AZ', 'AM', 'BG', 'J', '~CK', 'H'], ['CE', 'CN'], ['BN', '~CR', '~CI', '~U', '~D', 'S'],
	['AE', 'AI'], ['~BB', 'BQ'], ['~BI', 'BE', '~CC', 'AM', 'AJ'], ['BH', 'BD'], ['~BT', 'CU', '~CB', '~CA'],
	['~BI', 'AF', '~BG'], ['~R', 'BC'], ['~AL', 'AD', '~AU'], ['BR', 'CD'], ['CM', '~BQ', '~Q'],
]
truth_cnf_unsat = None

print(""""
### Evaluates these asserts:
### - assert(solver.solve_sat(cnf_sat, False) == truth_cnf_sat)
### - assert(solver.solve_sat(cnf_unsat, False) == truth_cnf_unsat)
### - assert(solver.solve_sat(cnf_sat_small, True) == truth_cnf_sat_small)
""")
# no errors - asserts passed - the solver is working
assert(solver.solve_sat(cnf_sat, False) == truth_cnf_sat)
assert(solver.solve_sat(cnf_unsat, False) == truth_cnf_unsat)
assert(solver.solve_sat(cnf_sat_small, True) == truth_cnf_sat_small)

print("\n### All tests passed")