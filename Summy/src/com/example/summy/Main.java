package com.example.summy;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.Menu;
import android.view.View;
import android.widget.Button;

public class Main extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		final Button button = (Button) findViewById(R.id.take_picture);
		button.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v){
				dispatchTakePictureIntent();
			}
		});
	}
	final int REQUEST_IMAGE_CAPTURE = 1;
	protected void dispatchTakePictureIntent(){
		Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
		if (takePictureIntent.resolveActivity(getPackageManager()) != null){
			startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
		}
	}
	
	protected void onAcitivityResult(int requestCode, int resultCode, Intent data){
		if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK){
			Bundle extras = data.getExtras();
			Bitmap imageBitmap = (Bitmap) extras.get("data");
			
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

}
