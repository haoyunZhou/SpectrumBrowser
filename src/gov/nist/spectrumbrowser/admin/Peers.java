package gov.nist.spectrumbrowser.admin;

import com.google.gwt.dev.json.JsonObject;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.json.client.JSONArray;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
import com.google.gwt.json.client.JSONValue;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.RadioButton;
import com.google.gwt.user.client.ui.TextBox;

import gov.nist.spectrumbrowser.common.AbstractSpectrumBrowserWidget;
import gov.nist.spectrumbrowser.common.SpectrumBrowserCallback;
import gov.nist.spectrumbrowser.common.SpectrumBrowserScreen;

public class Peers extends AbstractSpectrumBrowserWidget implements SpectrumBrowserCallback<String>, SpectrumBrowserScreen {
	Admin admin;
	private JSONObject jsonObject;
	private Grid grid;
	private boolean redraw;

	private class ButtonClickHandler implements ClickHandler {
		String host;
		int port;
		
		public ButtonClickHandler( String host, int port) {
			this.host = host;
			this.port = port;
		}

		@Override
		public void onClick(ClickEvent event) {
			redraw = true;
			Admin.getAdminService().removePeer(host,port,Peers.this);
		}
		
	}
	
	public Peers(Admin admin) {
		super();
		this.admin = admin;
		Admin.getAdminService().getPeers(this);
	}

	@Override
	public void onSuccess(String result) {
		try {
			jsonObject = JSONParser.parseLenient(result).isObject();
			if ( redraw) {
				draw();
			}
		} catch (Exception ex) {
			Window.alert("Error parsing result");
			admin.logoff();
		}
	
		
	}

	@Override
	public void onFailure(Throwable throwable) {
		Window.alert("Error contacting the web service");
		admin.logoff();
	}

	private void addPeer(int count, String host, int port, String protocol) {
		String url = protocol + "//" + host + ":" + port;
		grid.setText(count, 0, url);
		Button button = new Button("Delete");	
		grid.setWidget(count, 1,button );
		button.addClickHandler(new ButtonClickHandler(host,port));
		
	}
	@Override
	public void draw() {
		verticalPanel.clear();
		HTML html = new HTML("<h2>Destination for outbound Registration</h2>");
		JSONArray peers = jsonObject.get("peers").isArray();

		int rows = peers.size();
		verticalPanel.add(html);
		grid = new Grid(rows,2);
		verticalPanel.add(grid);
		for (int i = 0; i < peers.size(); i++) {
			JSONObject peer = peers.get(i).isObject();
			String host = peer.get("host").isString().stringValue();
			int port =(int) peer.get("port").isNumber().doubleValue();
			String protocol = peer.get("protocol").isString().stringValue();
			addPeer(i,host,port,protocol);			
		}
		Button addPeerButton = new Button("Add Peer");
		Button logoffButton = new Button ("Log Off");
		logoffButton.addClickHandler( new ClickHandler() {

			@Override
			public void onClick(ClickEvent event) {
				admin.logoff();
			}} );
		HorizontalPanel horizontalPanel = new HorizontalPanel();
		horizontalPanel.add(addPeerButton);
		horizontalPanel.add(logoffButton);
		
		addPeerButton.addClickHandler( new ClickHandler() {

			@Override
			public void onClick(ClickEvent event) {
				redraw = true;
				new AddPeer(admin, Peers.this, verticalPanel).draw();
				
			}} );
		
		verticalPanel.add(horizontalPanel);
	}

	@Override
	public String getLabel() {
		return null;
	}

	@Override
	public String getEndLabel() {
		return "Peers";
	}
}
