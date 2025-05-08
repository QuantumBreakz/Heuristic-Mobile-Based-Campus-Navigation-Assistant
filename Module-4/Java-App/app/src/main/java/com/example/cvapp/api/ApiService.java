package com.example.cvapp.api;

import com.example.cvapp.models.*;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.*;

import java.util.List;
import java.util.Map;

public interface ApiService {
    @Multipart
    @POST("recognize")
    Call<RecognitionResponse> recognizeBuilding(
        @Part MultipartBody.Part image,
        @Part("building_type") RequestBody buildingType
    );

    @Multipart
    @POST("distance")
    Call<DistanceResponse> estimateDistance(
        @Part MultipartBody.Part image,
        @Part("building_type") RequestBody buildingType
    );

    @Multipart
    @POST("position")
    Call<PositionResponse> trackPosition(
        @Part MultipartBody.Part image
    );

    @GET("buildings")
    Call<BuildingsResponse> getBuildings();

    @Multipart
    @POST("train")
    Call<TrainingResponse> trainModel(
        @Part MultipartBody.Part image,
        @Part("building_name") RequestBody buildingName,
        @Part("building_type") RequestBody buildingType
    );

    @Multipart
    @POST("calibrate")
    Call<CalibrationResponse> calibrateDistance(@Body CalibrationRequest request);

    @POST("building_types")
    Call<BuildingTypesResponse> getBuildingTypes();

    @POST("update_landmark")
    Call<LandmarkResponse> updateLandmarkPosition(
        @Query("building_name") String buildingName,
        @Body Coordinates position
    );

    @GET("position_history")
    Call<PositionHistoryResponse> getPositionHistory();

    @POST("reset_position_history")
    Call<BaseResponse> resetPositionHistory();

    @GET("visualization")
    Call<VisualizationResponse> getVisualization();

    @POST("visualization_config")
    Call<VisualizationConfigResponse> updateVisualizationConfig(@Body VisualizationConfigRequest config);
} 