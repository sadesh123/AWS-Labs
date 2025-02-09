package dns

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
)

// Function to load the environment variables from the .env file
func LoadEnv() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
}

// Function to get the WHOIS API key from the environment
func GetAPIKey() string {
	apiKey := os.Getenv("<Your-Environment-Variable-Name>")
	if apiKey == "" {
		log.Fatal("WHOIS API key is missing")
	}
	return apiKey
}

// Define the WHOIS API URL
const whoisAPIURL = "https://api.apilayer.com/whois/check?domain="

// ValidateDomain sends a GET request to the WHOIS API to check the domain
func ValidateDomain(domain string) (string, error) {
	// Load the environment variables (and get the API key)
	LoadEnv()

	// Get the API key from environment
	whoisAPIKey := GetAPIKey()

	// Create a new HTTP client and request
	client := &http.Client{}
	req, err := http.NewRequest("GET", whoisAPIURL+domain, nil)
	if err != nil {
		return "", fmt.Errorf("error creating request: %v", err)
	}

	// Set the authentication header with the API key
	req.Header.Add("apikey", whoisAPIKey)

	// Perform the GET request
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("error making request: %v", err)
	}
	defer resp.Body.Close()

	// Log response status and URL for debugging
	log.Printf("Request URL: %s", req.URL)
	log.Printf("Response Status Code: %d", resp.StatusCode)

	// Check the response status code
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("received non-OK status code %d", resp.StatusCode)
	}

	// Read the response body using io.ReadAll instead of ioutil.ReadAll
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("error reading response body: %v", err)
	}

	// Log the raw response body to inspect it
	log.Printf("Response Body: %s", string(body))

	// Return the WHOIS data as a string
	return string(body), nil
}
