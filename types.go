package main

// APIService struct from response
type APIService struct {
	MongoID struct {
		Oid string `json:"$oid"`
	} `json:"_id"`
	Name           string   `json:"name"`
	Description    string   `json:"description"`
	StartCommand   string   `json:"start_command"`
	StopCommand    string   `json:"stop_command"`
	RestartCommand string   `json:"restart_command"`
	StatusCommand  string   `json:"status_command"`
	LogCommand     string   `json:"log_command"`
	ID             string   `json:"id"`
	AssociatedTo   string   `json:"associated_to"`
	Logs           []string `json:"logs"`
}

// ServerPayload datatype for outgoing log messages
type ServerPayload struct {
	Heartbeat bool   `json:"heartbeat"`
	ServiceID string `json:"service_id"`
	Log       string `json:"log"`
}

// AuthenticationDetails to feed to each socket
type AuthenticationDetails struct {
	UserID    string
	AuthToken string
}

// ServerAuthRequest for when each socket authenticates
type ServerAuthRequest struct {
	AuthToken string `json:"auth_token"`
	UserID    string `json:"user_id"`
	ServiceID string `json:"service_id"`
}
