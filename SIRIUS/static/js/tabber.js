// Function that shows the activeTab and hides the rest
function refreshTabs(activeTab){
	var tabButtons = $('div#tabber_buttons').children();
	var heuristicID;
	$('div[id^=tabber_tab_]').each(function(index, tab){
		heuristicID = $(this).attr('id').split('_');
		heuristicID = heuristicID[heuristicID.length-1]
		if(heuristicID == activeTab){
			$(tab).show();
			$(tabButtons[index]).addClass('activeTab');
		}else{
			$(tab).hide();
			$(tabButtons[index]).removeClass('activeTab');
		}
	});
}

// Function that validates the form before submitting
function validateForm(){
	var inputs = $('*#input_group');
	
	// Looping through input_groups
	inputs.each(function(){
		
		// Looping through each element of input_group
		var input;
		var checked = false;
		$(this).children().each(function(){
			input = $(this).children()[1].childNodes[0];
			if(input.checked){
				checked = true;
				return false; //this breaks outside of the loop
			}
		});
		
		// If there are no checked inputs in this group, go to that page
		if(!checked){
			var input_tab = input.name.split('_')[1];
			var tabButtons = $('div#tabber_buttons').children();
			tabButtons.each(function(){
				if($(this).attr('id').split('_')[2] == input_tab){
					$(this)[0].click();
					return false;
				}
			});
			return false; 
		}
	});
}

$(document).ready(function createTabber(){
	var tabs = $('div[id^=tabber_tab_]');
	var heuristicPks = [];
	var nTabs = tabs.length;
	console.log('ntabs: '+nTabs);
	var currentTab = 0;
	
	// Creating tabButtons
	var tabButtons = $('div#tabber_buttons');
	var heuristicID;
	$(tabs).each(function(){
		heuristicID = $(this).attr('id').split('_');
		heuristicID = heuristicID[heuristicID.length-1];
		var tabName = $('div#tabber_tab_'+heuristicID+' #tabName').text();
		tabName = tabName.slice(0, tabName.length-1);
		tabButtons.append(
			'<button id="tabber_button_'+heuristicID+'"\
					 class="btn azulito"\
					 type="button" \
					 onclick="refreshTabs('+heuristicID+')">\
					 '+tabName+'\
					 </button>'
		);
	})
	
	// Hiding unactive tabs
	tabs.each(function(index, tab){
		if(index != currentTab){				
			$(tab).hide();
		}
	});
	
	// Selecting focus for the current active button
	tabButtons.children().each(function(index, button){
		if(index == currentTab){
			$(button).addClass('activeTab');
		} else {
			$(button).removeClass('activeTab');
		}
	});
});
