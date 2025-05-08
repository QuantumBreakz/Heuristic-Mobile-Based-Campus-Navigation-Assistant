package com.example.cvapp.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.cvapp.R;
import com.example.cvapp.models.Building;

import java.util.List;

public class BuildingAdapter extends RecyclerView.Adapter<BuildingAdapter.BuildingViewHolder> {
    private List<Building> buildings;

    public BuildingAdapter(List<Building> buildings) {
        this.buildings = buildings;
    }

    public void updateBuildings(List<Building> newBuildings) {
        this.buildings = newBuildings;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public BuildingViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_building, parent, false);
        return new BuildingViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull BuildingViewHolder holder, int position) {
        Building building = buildings.get(position);
        holder.nameText.setText(building.getName());
        holder.typeText.setText(building.getType());
        holder.coordinatesText.setText(String.format("Location: %.6f, %.6f",
                building.getCoordinates().getLatitude(),
                building.getCoordinates().getLongitude()));
    }

    @Override
    public int getItemCount() {
        return buildings.size();
    }

    static class BuildingViewHolder extends RecyclerView.ViewHolder {
        TextView nameText;
        TextView typeText;
        TextView coordinatesText;

        BuildingViewHolder(View itemView) {
            super(itemView);
            nameText = itemView.findViewById(R.id.buildingName);
            typeText = itemView.findViewById(R.id.buildingType);
            coordinatesText = itemView.findViewById(R.id.buildingCoordinates);
        }
    }
} 