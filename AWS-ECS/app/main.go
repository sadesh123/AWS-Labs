package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"phishing-detector/internal/detector" // Use the detector package directly
)

type ApiResponse struct {
	Domain         string `json:"domain"`
	WhoisData      string `json:"whois_data,omitempty"`
	Error          string `json:"error,omitempty"`
	PhishingStatus string `json:"phishing_status"` // New field for phishing status
}

func main() {
	// Serve static files (like index.html) from the /public folder
	http.Handle("/public/", http.StripPrefix("/public/", http.FileServer(http.Dir("./public"))))

	// Define an API route to validate domain
	http.HandleFunc("/validate-domain", func(w http.ResponseWriter, r *http.Request) {
		domain := r.URL.Query().Get("domain")
		if domain == "" {
			http.Error(w, "Domain is required", http.StatusBadRequest)
			return
		}

		// Check phishing status and get WHOIS data if necessary
		phishingStatus, whoisData := detector.CheckPhishingEmail(domain)

		// Construct the API response
		response := ApiResponse{
			Domain:         domain,
			PhishingStatus: phishingStatus,
			WhoisData:      whoisData,
		}

		// Respond with the JSON data
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	// Start the HTTP server
	port := "8080"
	fmt.Println("Server is running on port", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
