app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://agent-gold-three.vercel.app",
        "https://aware-trust-production-734d.up.railway.app",
        "http://localhost:3000",
        "*"  # Temporary for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
