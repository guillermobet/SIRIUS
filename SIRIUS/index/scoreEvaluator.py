#
#	cf: Correction Factor
#	up: Usability Percentage
#


def get_cf(criterion, criteria, website_type):
	relevance = criterion.meta_criteria.get_relevance_list()[website_type]
	relevance_value = criterion_relevance_mapping[relevance]
	denominator = 0
	
	for crit in criteria:
		if(crit.value != 'NA'):
			relevance = crit.meta_criteria.get_relevance_list()[website_type]
			#denominator += crit.meta_criteria.get_relevance_list()[website_type]
			denominator += criterion_relevance_mapping[relevance]
			
	cf = relevance_value / denominator
	return cf

def get_up(criteria, website_type):
	numerator = 0
	denominator = 0
	
	for crit in criteria:
		if(crit.value != 'NA'):
			cf = get_cf(crit, criteria, website_type)
			numerator += cf * crit.get_numeric_value()
			denominator += cf * 10
			
	pu = (numerator/denominator)*100
	return pu
	

qualitative_mapping = {
	'NTS' : 0,
	'NEP' : 2.5,
	'NPP' : 5,
	'NPI' : 7.5,
	'S' : 10,
	}
	
heuristic_relevance_mapping = {
	'Muy alta' : 4,
	'Alta' : 3,
	'Media' : 2,
	'Baja' : 1
}

criterion_relevance_mapping = {
	'CR' : 8,
	'MA' : 4,
	'ME' : 2,
	'MO' : 1
}


