package types

type Db struct {
	Addr   string
	User   string
	Pwd    string
	Hits   string
	Events string
}

type RedisDb struct {
	Addr string
	Name int
}

type Event struct {
	Id          string
	Name        string
	Class       string
	ObjPk       string
	ContentType string
	User        string
	Url         string
	AdminUrl    string
	Notes       string
	Request     string
	Service     string
	Bucket      string
	Data        string
}

type Hit struct {
	Id              string
	Domain          string
	Path            string
	Method          string
	Ip              string
	UserAgent       string
	IsAuthenticated string
	IsStaff         string
	IsSuperuser     string
	User            string
	Referer         string
	View            string
	Module          string
	StatusCode      string
	ReasonPhrase    string
	RequestTime     string
	ContentLength   string
	NumQueries      string
	QueriesTime     string
}
