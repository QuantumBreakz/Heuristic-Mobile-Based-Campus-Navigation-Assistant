package com.example.cvapp;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.location.Location;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureException;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;

import com.example.cvapp.adapters.BuildingAdapter;
import com.example.cvapp.api.ApiClient;
import com.example.cvapp.api.ApiService;
import com.example.cvapp.databinding.ActivityMainBinding;
import com.example.cvapp.models.*;
import com.example.cvapp.utils.*;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.Priority;
import com.google.android.gms.tasks.CancellationToken;
import com.google.android.gms.tasks.CancellationTokenSource;
import com.google.android.gms.tasks.OnTokenCanceledListener;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.android.material.button.MaterialButton;
import com.google.gson.Gson;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executor;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private static final int CAMERA_REQUEST_CODE = 100;
    private static final int PERMISSION_REQUEST_CODE = 200;
    private ActivityMainBinding binding;
    private ApiService apiService;
    private FusedLocationProviderClient fusedLocationClient;
    private BuildingAdapter buildingAdapter;
    private List<Building> buildings = new ArrayList<>();
    private List<String> buildingTypes = new ArrayList<>();
    private Handler handler = new Handler(Looper.getMainLooper());
    private boolean isProcessing = false;
    private File currentPhotoFile;
    private static final int LOCATION_UPDATE_INTERVAL = 1000; // 1 second
    private ImageCapture imageCapture;
    private Executor cameraExecutor;
    private VisualizationConfig visualizationConfig;

    private final ActivityResultLauncher<String[]> requestPermissionLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestMultiplePermissions(), result -> {
                boolean allGranted = true;
                for (Boolean granted : result.values()) {
                    if (!granted) {
                        allGranted = false;
                        break;
                    }
                }
                if (allGranted) {
                    initializeLocationServices();
                    initializeCamera();
                } else {
                    UIUtils.showLongToast(this, getString(R.string.permissions_required));
                }
            });

    private final ActivityResultLauncher<Intent> takePictureLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Bundle extras = result.getData().getExtras();
                    Bitmap imageBitmap = (Bitmap) extras.get("data");
                    processImage(imageBitmap);
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // Initialize camera executor
        cameraExecutor = ContextCompat.getMainExecutor(this);

        // Initialize API service
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://10.0.2.2:5000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        apiService = retrofit.create(ApiService.class);

        // Initialize visualization config
        visualizationConfig = new VisualizationConfig(
            new int[]{10, 10}, // figureSize
            100, // dpi
            5, // markerSize
            2.0f, // historyLineWidth
            100, // updateInterval
            true, // showGrid
            true, // showLegend
            true  // showConfidence
        );

        initializeComponents();
        checkPermissions();
        setupUI();
        loadBuildingTypes();
        loadBuildings();
        startPositionUpdates();
    }

    private void initializeComponents() {
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        buildingAdapter = new BuildingAdapter(buildings);
    }

    private void checkPermissions() {
        if (!PermissionUtils.hasRequiredPermissions(this)) {
            requestPermissionLauncher.launch(PermissionUtils.REQUIRED_PERMISSIONS);
        } else {
            initializeLocationServices();
            initializeCamera();
        }
    }

    private void setupUI() {
        // Building Type Spinner
        AutoCompleteTextView buildingTypeSpinner = findViewById(R.id.building_type_spinner);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_dropdown_item_1line,
                new String[]{"Academic", "Administrative", "Residential"});
        buildingTypeSpinner.setAdapter(adapter);

        // Set up reset position button
        MaterialButton resetPositionButton = findViewById(R.id.reset_position_button);
        resetPositionButton.setOnClickListener(v -> resetPositionHistory());
    }

    private void initializeLocationServices() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            startPositionUpdates();
        }
    }

    private void initializeCamera() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            startCamera();
        }
    }

    private void startCamera() {
        ListenableFuture<ProcessCameraProvider> cameraProviderFuture = ProcessCameraProvider.getInstance(this);

        cameraProviderFuture.addListener(() -> {
            try {
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();

                Preview preview = new Preview.Builder().build();
                androidx.camera.view.PreviewView previewView = findViewById(R.id.camera_preview);
                preview.setSurfaceProvider(previewView.getSurfaceProvider());

                imageCapture = new ImageCapture.Builder()
                        .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                        .build();

                CameraSelector cameraSelector = new CameraSelector.Builder()
                        .requireLensFacing(CameraSelector.LENS_FACING_BACK)
                        .build();

                cameraProvider.unbindAll();
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageCapture);

            } catch (ExecutionException | InterruptedException e) {
                Log.e(TAG, "Error starting camera", e);
            }
        }, cameraExecutor);
    }

    private void captureImage() {
        if (imageCapture == null) return;

        imageCapture.takePicture(cameraExecutor, new ImageCapture.OnImageCapturedCallback() {
            public void onCaptureSuccess(@NonNull ImageCapture.OutputFileResults output) {
                processImage(output.getSavedUri());
            }

            @Override
            public void onError(@NonNull ImageCaptureException exception) {
                Log.e(TAG, "Error capturing image", exception);
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Error capturing image", Toast.LENGTH_SHORT).show());
            }
        });
    }

    private void processImage(Bitmap bitmap) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
            byte[] imageBytes = baos.toByteArray();

            RequestBody requestFile = RequestBody.create(MediaType.parse("image/*"), imageBytes);
            MultipartBody.Part body = MultipartBody.Part.createFormData("file", "image.jpg", requestFile);

            // Get selected building type
            AutoCompleteTextView buildingTypeSpinner = findViewById(R.id.building_type_spinner);
            String selectedType = buildingTypeSpinner.getText().toString();
            RequestBody buildingTypeBody = RequestBody.create(MediaType.parse("text/plain"), selectedType);

            // Make API calls
            recognizeBuilding(body, buildingTypeBody);
            estimateDistance(body, buildingTypeBody);
            trackPosition(body);

        } catch (Exception e) {
            Log.e(TAG, "Error processing image", e);
            Toast.makeText(this, "Error processing image", Toast.LENGTH_SHORT).show();
        }
    }

    private void processImage(Uri imageUri) {
        try {
            Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
            processImage(bitmap);
        } catch (IOException e) {
            Log.e(TAG, "Error loading image from URI", e);
            Toast.makeText(this, "Error loading image", Toast.LENGTH_SHORT).show();
        }
    }

    private void recognizeBuilding(MultipartBody.Part image, RequestBody buildingType) {
        apiService.recognizeBuilding(image, buildingType).enqueue(new Callback<RecognitionResponse>() {
            @Override
            public void onResponse(Call<RecognitionResponse> call, Response<RecognitionResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    RecognitionResponse result = response.body();
                    updateRecognitionResult(result);
                }
            }

            @Override
            public void onFailure(Call<RecognitionResponse> call, Throwable t) {
                Log.e(TAG, "Error recognizing building", t);
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Error recognizing building", Toast.LENGTH_SHORT).show());
            }
        });
    }

    private void estimateDistance(MultipartBody.Part image, RequestBody buildingType) {
        apiService.estimateDistance(image, buildingType).enqueue(new Callback<DistanceResponse>() {
            @Override
            public void onResponse(Call<DistanceResponse> call, Response<DistanceResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    DistanceResponse result = response.body();
                    updateDistanceResult(result);
                }
            }

            @Override
            public void onFailure(Call<DistanceResponse> call, Throwable t) {
                Log.e(TAG, "Error estimating distance", t);
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Error estimating distance", Toast.LENGTH_SHORT).show());
            }
        });
    }

    private void trackPosition(MultipartBody.Part image) {
        apiService.trackPosition(image).enqueue(new Callback<PositionResponse>() {
            @Override
            public void onResponse(Call<PositionResponse> call, Response<PositionResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    PositionResponse result = response.body();
                    updatePositionResult(result);
                }
            }

            @Override
            public void onFailure(Call<PositionResponse> call, Throwable t) {
                Log.e(TAG, "Error tracking position", t);
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Error tracking position", Toast.LENGTH_SHORT).show());
            }
        });
    }

    private void updateRecognitionResult(RecognitionResponse result) {
        runOnUiThread(() -> {
            TextView recognitionResult = findViewById(R.id.recognition_result);
            recognitionResult.setText(String.format("Building: %s\nType: %s", 
                result.getBuildingName(), result.getBuildingType()));
        });
    }

    private void updateDistanceResult(DistanceResponse result) {
        runOnUiThread(() -> {
            TextView distanceResult = findViewById(R.id.distance_result);
            distanceResult.setText(String.format("Distance: %.2f meters", result.getDistance()));
        });
    }

    private void updatePositionResult(PositionResponse result) {
        runOnUiThread(() -> {
            TextView positionResult = findViewById(R.id.position_result);
            positionResult.setText(String.format("Position: (%.6f, %.6f)", 
                result.getCurrentPosition().getLatitude(), 
                result.getCurrentPosition().getLongitude()));
        });
    }

    private void resetPositionHistory() {
        apiService.resetPositionHistory().enqueue(new Callback<BaseResponse>() {
            @Override
            public void onResponse(Call<BaseResponse> call, Response<BaseResponse> response) {
                if (response.isSuccessful()) {
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "Position history reset", Toast.LENGTH_SHORT).show());
                }
            }

            @Override
            public void onFailure(Call<BaseResponse> call, Throwable t) {
                Log.e(TAG, "Error resetting position history", t);
                runOnUiThread(() -> Toast.makeText(MainActivity.this, "Error resetting position history", Toast.LENGTH_SHORT).show());
            }
        });
    }

    private void startPositionUpdates() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if (ActivityCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                    fusedLocationClient.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, new CancellationToken() {
                        @Override
                        public CancellationToken onCanceledRequested(@NonNull OnTokenCanceledListener listener) {
                            return new CancellationTokenSource().getToken();
                        }

                        @Override
                        public boolean isCancellationRequested() {
                            return false;
                        }
                    }).addOnSuccessListener(location -> {
                        if (location != null) {
                            updatePosition(location);
                        }
                    });
                }
                handler.postDelayed(this, LOCATION_UPDATE_INTERVAL);
            }
        }, LOCATION_UPDATE_INTERVAL);
    }

    private void updatePosition(Location location) {
        Map<String, Double> distances = new HashMap<>();
        Map<String, Double> confidences = new HashMap<>();

        // Calculate distances to known buildings
        for (Building building : buildings) {
            double distance = LocationUtils.calculateDistance(
                    location.getLatitude(), location.getLongitude(),
                    building.getCoordinates().getLatitude(), building.getCoordinates().getLongitude()
            );
            distances.put(building.getName(), distance);
            confidences.put(building.getName(), 1.0); // Full confidence for now
        }

        // Create request body for the position update
        String jsonString = new Gson().toJson(new PositionUpdateRequest(distances, confidences));
        RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), jsonString);
        MultipartBody.Part body = MultipartBody.Part.createFormData("data", "position.json", requestBody);

        apiService.trackPosition(body).enqueue(new Callback<PositionResponse>() {
            @Override
            public void onResponse(Call<PositionResponse> call, Response<PositionResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    PositionResponse positionResponse = response.body();
                    updatePositionResult(positionResponse);
                }
            }

            @Override
            public void onFailure(Call<PositionResponse> call, Throwable t) {
                // Silent failure for position updates
            }
        });
    }

    private void loadBuildingTypes() {
        apiService.getBuildingTypes().enqueue(new Callback<BuildingTypesResponse>() {
            @Override
            public void onResponse(Call<BuildingTypesResponse> call, Response<BuildingTypesResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    buildingTypes.clear();
                    buildingTypes.add("All Types");
                    buildingTypes.addAll(response.body().getTypes());
                    AutoCompleteTextView buildingTypeSpinner = findViewById(R.id.building_type_spinner);
                    ArrayAdapter<String> adapter = new ArrayAdapter<>(
                        MainActivity.this,
                        android.R.layout.simple_dropdown_item_1line,
                        buildingTypes
                    );
                    buildingTypeSpinner.setAdapter(adapter);
                } else {
                    UIUtils.showToast(MainActivity.this, getString(R.string.error_loading_building_types));
                }
            }

            @Override
            public void onFailure(Call<BuildingTypesResponse> call, Throwable t) {
                UIUtils.showToast(MainActivity.this, getString(R.string.error_loading_building_types));
            }
        });
    }

    private void loadBuildings() {
        apiService.getBuildings().enqueue(new Callback<BuildingsResponse>() {
            @Override
            public void onResponse(Call<BuildingsResponse> call, Response<BuildingsResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Map<String, Building> buildingsMap = response.body().getBuildings();
                    buildings.clear();
                    buildings.addAll(buildingsMap.values());
                    buildingAdapter.updateBuildings(buildings);
                } else {
                    UIUtils.showToast(MainActivity.this, getString(R.string.error_loading_buildings));
                }
            }

            @Override
            public void onFailure(Call<BuildingsResponse> call, Throwable t) {
                UIUtils.showToast(MainActivity.this, getString(R.string.error_loading_buildings));
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        handler.removeCallbacksAndMessages(null);
        if (currentPhotoFile != null) {
            CameraUtils.deleteImageFile(currentPhotoFile);
        }
        cameraExecutor = null;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == R.id.action_settings) {
            startActivity(new Intent(this, SettingsActivity.class));
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
