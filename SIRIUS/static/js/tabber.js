// Function that shows the activeTab and hides the rest
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