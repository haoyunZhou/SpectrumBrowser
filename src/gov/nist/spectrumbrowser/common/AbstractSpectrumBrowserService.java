package gov.nist.spectrumbrowser.common;

import java.util.logging.Logger;

import com.google.gwt.core.client.GWT;
import com.google.gwt.http.client.Request;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.http.client.RequestCallback;
import com.google.gwt.http.client.Response;
import com.google.gwt.http.client.URL;
import com.google.gwt.user.client.Window;

public abstract class AbstractSpectrumBrowserService {
	protected String baseUrl;
	private static Logger logger = Logger.getLogger("SpectrumBrowser");
	
	class MyCallback implements RequestCallback {
		public SpectrumBrowserCallback<String> callback;

		public MyCallback(SpectrumBrowserCallback<String> callback) {
			this.callback = callback;
		}

		@Override
		public void onResponseReceived(Request request, Response response) {
			int status = response.getStatusCode();
			if (status == 200) {
				callback.onSuccess(response.getText());
			} else {
				callback.onFailure(new Exception("Error response " + status));
			}
		}

		@Override
		public void onError(Request request, Throwable exception) {
			callback.onFailure(exception);
		}

	}
	


	protected void dispatch(String uri, SpectrumBrowserCallback<String> callback) {
		try {
			String rawUrl = baseUrl + uri;
			String url = URL.encode(rawUrl);
			logger.finer("URL = " + url);
			RequestBuilder requestBuilder = new RequestBuilder(
					RequestBuilder.POST, url);
			requestBuilder.setCallback(new MyCallback(callback));
			requestBuilder.send();
		} catch (Exception ex) {
		}
	}
	
	public void authenticate(String userName, String password, String privilege, SpectrumBrowserCallback<String> callback)
			throws IllegalArgumentException {

		String uri = "authenticate/" + privilege + "/" + userName
				+ "?password=" + password;

		dispatch(uri, callback);

	}
	
	public void logOut(String sessionId,
			SpectrumBrowserCallback<String> callback)
			throws IllegalArgumentException {
		String uri = "logOut/" + sessionId;
		dispatch(uri, callback);
	}
	

}
