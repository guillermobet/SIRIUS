// Function that shows the activeTab and hides the rest
function refreshTabs(activeTab){
	var tabButtons = $('div#tabber_buttons').children();
	$('div[id^=tabber_tab]').each(function(index, tab){
		if(index == activeTab){
			$(tab).show();
			$(tabButtons[index]).addClass('activeTab');
		}else{
			$(tab).hide();
			$(tabButtons[index]).removeClass('activeTab');
		}
	});
}

$(document).ready(function(){
	var tabs = $('div[id^=tabber_tab]');
	var nTabs = tabs.length;
	var currentTab = 0;
	
	// Creating tabButtons
	var tabButtons = $('div#tabber_buttons');
	var i = 0;
	for(i = 0; i < nTabs; i++){
		var tabName = $('div#tabber_tab'+i+' h3').text();
		tabName = tabName.slice(0, tabName.length-1);
		tabButtons.append(
			'<button id="tabber_button_'+i+'"\
					 class="btn azulito"\
					 type="button" \
					 onclick="refreshTabs('+i+')">\
					 '+tabName+'\
					 </button>'
		);
	}
	
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
