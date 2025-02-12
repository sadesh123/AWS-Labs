package main

import (
	"context"
	"encoding/json"
	"net/http"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

// Shot represents an NBA player's shot attempt
type Shot struct {
	ID       string  `json:"id"`
	PlayerID string  `json:"player_id"`
	Player   string  `json:"player"`
	Team     string  `json:"team"`
	GameDate string  `json:"game_date"`
	Quarter  int     `json:"quarter"`
	TimeLeft string  `json:"time_left"`
	X        float64 `json:"x"`
	Y        float64 `json:"y"`
	ShotType string  `json:"shot_type"`
	Outcome  string  `json:"outcome"`
}

// Seed data - a list of shots
var shots = []Shot{
	{ID: "1", PlayerID: "23", Player: "LeBron James", Team: "Lakers", GameDate: "2024-02-10", Quarter: 1, TimeLeft: "10:30", X: 25.5, Y: 15.2, ShotType: "3PT", Outcome: "Made"},
	{ID: "2", PlayerID: "30", Player: "Stephen Curry", Team: "Warriors", GameDate: "2024-02-10", Quarter: 2, TimeLeft: "05:45", X: 27.3, Y: 14.8, ShotType: "3PT", Outcome: "Missed"},
	{ID: "3", PlayerID: "34", Player: "Giannis Antetokounmpo", Team: "Bucks", GameDate: "2024-02-10", Quarter: 3, TimeLeft: "07:20", X: 10.2, Y: 5.6, ShotType: "2PT", Outcome: "Made"},
}

// Lambda handler function
func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	switch request.HTTPMethod {
	case "GET":
		if request.Resource == "/shots" {
			return getShots()
		} else if request.Resource == "/shots/{player_id}" {
			playerID := request.PathParameters["player_id"]
			return getShotsByPlayer(playerID)
		}
	case "POST":
		if request.Resource == "/shots" {
			return postShot(request.Body)
		}
	}

	return events.APIGatewayProxyResponse{
		StatusCode: http.StatusNotFound,
		Body:       `{"message": "Not Found"}`,
		Headers:    map[string]string{"Content-Type": "application/json"},
	}, nil
}

// Get all shots
func getShots() (events.APIGatewayProxyResponse, error) {
	body, _ := json.Marshal(shots)
	return events.APIGatewayProxyResponse{
		StatusCode: http.StatusOK,
		Body:       string(body),
		Headers:    map[string]string{"Content-Type": "application/json"},
	}, nil
}

// Get shots by Player ID
func getShotsByPlayer(playerID string) (events.APIGatewayProxyResponse, error) {
	var playerShots []Shot

	for _, shot := range shots {
		if shot.PlayerID == playerID {
			playerShots = append(playerShots, shot)
		}
	}

	if len(playerShots) == 0 {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusNotFound,
			Body:       `{"message": "No shots found for this player"}`,
			Headers:    map[string]string{"Content-Type": "application/json"},
		}, nil
	}

	body, _ := json.Marshal(playerShots)
	return events.APIGatewayProxyResponse{
		StatusCode: http.StatusOK,
		Body:       string(body),
		Headers:    map[string]string{"Content-Type": "application/json"},
	}, nil
}

// Add a new shot
func postShot(body string) (events.APIGatewayProxyResponse, error) {
	var newShot Shot
	err := json.Unmarshal([]byte(body), &newShot)
	if err != nil {
		return events.APIGatewayProxyResponse{
			StatusCode: http.StatusBadRequest,
			Body:       `{"error": "Invalid request body"}`,
			Headers:    map[string]string{"Content-Type": "application/json"},
		}, nil
	}

	shots = append(shots, newShot)

	responseBody, _ := json.Marshal(newShot)
	return events.APIGatewayProxyResponse{
		StatusCode: http.StatusCreated,
		Body:       string(responseBody),
		Headers:    map[string]string{"Content-Type": "application/json"},
	}, nil
}

func main() {
	lambda.Start(handler)
}
