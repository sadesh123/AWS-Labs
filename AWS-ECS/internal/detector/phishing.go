package detector

import (
	"fmt"
	"net/mail" // Package for email address parsing
	"phishing-detector/internal/dns"
	"regexp"
	"strings"
)

// List of known safe domains (expand this list)
var safeDomains = []string{
	"paypal.com", "amazon.com", "bankofamerica.com", "google.com",
}

// Suspicious keyword patterns
var phishingPatterns = []string{
	`(?i)secure`, `(?i)update`, `(?i)support`, `(?i)alert`,
	`(?i)account`, `(?i)verify`, `(?i)banking`, `(?i)login`,
	`\d{3,}`, // Emails with random numbers
}

// Extracts domain from an email (e.g., "test@paypal.com" → "paypal.com")
// If it's a regular domain, returns the domain directly
func extractDomain(input string) (string, error) {
	// If the input contains an "@" symbol, treat it as an email address
	if strings.Contains(input, "@") {
		// Validate the email format using the mail package
		_, err := mail.ParseAddress(input)
		if err != nil {
			return "", fmt.Errorf("invalid email format: %s", input)
		}

		parts := strings.Split(input, "@")
		if len(parts) == 2 {
			return parts[1], nil
		}
		return "", fmt.Errorf("failed to extract domain from email: %s", input)
	}

	// If the input doesn't contain "@", treat it as a domain
	return input, nil
}

// Compute Levenshtein Distance between two strings
func levenshteinDistance(s1, s2 string) int {
	s1Len := len(s1)
	s2Len := len(s2)

	// If either string is empty, return the length of the other
	if s1Len == 0 {
		return s2Len
	}
	if s2Len == 0 {
		return s1Len
	}

	// Create a DP table
	matrix := make([][]int, s1Len+1)
	for i := range matrix {
		matrix[i] = make([]int, s2Len+1)
	}

	// Initialize base cases
	for i := 0; i <= s1Len; i++ {
		matrix[i][0] = i
	}
	for j := 0; j <= s2Len; j++ {
		matrix[0][j] = j
	}

	// Fill DP table
	for i := 1; i <= s1Len; i++ {
		for j := 1; j <= s2Len; j++ {
			cost := 0
			if s1[i-1] != s2[j-1] {
				cost = 1
			}
			matrix[i][j] = min(
				matrix[i-1][j]+1,      // Deletion
				matrix[i][j-1]+1,      // Insertion
				matrix[i-1][j-1]+cost, // Substitution
			)
		}
	}

	return matrix[s1Len][s2Len]
}

// Helper function to get the minimum of three numbers
func min(a, b, c int) int {
	if a < b && a < c {
		return a
	}
	if b < c {
		return b
	}
	return c
}

// Check if a domain is a typosquatted version of a safe domain
func isTyposquattedDomain(domain string) bool {
	for _, safe := range safeDomains {
		if levenshteinDistance(domain, safe) <= 2 { // Allow small typo differences
			return true
		}
	}
	return false
}

// Check if the email is phishing based on patterns, domain, or typosquatting
func CheckPhishingEmail(input string) (string, string) {
	// Convert to lowercase to handle case insensitivity
	input = strings.ToLower(input)
	domain, err := extractDomain(input)

	// Log extracted domain and email being checked
	fmt.Println("Checking input:", input)

	// If domain extraction failed, return error
	if err != nil {
		fmt.Println("Error extracting domain:", err)
		return "invalid input", err.Error()
	}

	fmt.Println("Extracted domain:", domain)

	// First, check if the domain is in the safe list
	if isSafeDomain(domain) {
		// If domain is safe, return not phishing immediately
		fmt.Println("Domain is safe:", domain)
		return "not phishing", "" // Ensure that we return here if the domain is safe
	}

	// Check for phishing patterns in email address or domain
	for _, pattern := range phishingPatterns {
		match, _ := regexp.MatchString(pattern, input)
		if match {
			fmt.Println("Phishing pattern match found:", pattern)
			return "likely phishing", "" // Return phishing status without WHOIS data
		}
	}

	// Check if domain is typosquatted
	if isTyposquattedDomain(domain) {
		fmt.Println("Domain is typosquatted:", domain)
		return "likely phishing", ""
	}

	// If the domain isn't safe, check WHOIS
	whoisData, err := dns.ValidateDomain(domain)
	if err != nil {
		fmt.Println("Error validating domain with WHOIS:", err)
		return "likely phishing", err.Error()
	}

	// If WHOIS data indicates the domain is registered, it might not be phishing
	if whoisData != "" && whoisData != "not registered" {
		fmt.Println("WHOIS data for domain:", domain, "Registered")
		return "not phishing", whoisData
	}

	// If domain is not registered or suspicious, it's likely phishing
	fmt.Println("Domain is not registered or suspicious:", domain)
	return "likely phishing", whoisData
}

// isSafeDomain checks if the domain exists in our safe list
func isSafeDomain(domain string) bool {
	for _, safe := range safeDomains {
		if domain == safe {
			return true
		}
	}
	return false
}
