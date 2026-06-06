---
name: authentication-patterns
description: Authentication and authorization patterns including OAuth2, JWT, RBAC, session management, and PKCE flows
---

# Authentication Patterns

## JWT Access and Refresh Tokens

```typescript
import jwt from "jsonwebtoken";

interface TokenPayload {
  sub: string;
  email: string;
  roles: string[];
}

function generateTokens(user: User) {
  const accessToken = jwt.sign(
    { sub: user.id, email: user.email, roles: user.roles },
    process.env.JWT_SECRET!,
    { expiresIn: "15m", issuer: "auth-service" }
  );

  const refreshToken = jwt.sign(
    { sub: user.id, tokenVersion: user.tokenVersion },
    process.env.REFRESH_SECRET!,
    { expiresIn: "7d", issuer: "auth-service" }
  );

  return { accessToken, refreshToken };
}

function verifyAccessToken(token: string): TokenPayload {
  return jwt.verify(token, process.env.JWT_SECRET!, {
    issuer: "auth-service",
  }) as TokenPayload;
}
```

Short-lived access tokens (15 minutes) with longer-lived refresh tokens (7 days). Store refresh tokens in HTTP-only cookies.

## Auth Middleware

```typescript
function authenticate(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header?.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing authorization header" });
  }

  try {
    const payload = verifyAccessToken(header.slice(7));
    req.user = payload;
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      return res.status(401).json({ error: "Token expired" });
    }
    return res.status(401).json({ error: "Invalid token" });
  }
}

function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) return res.status(401).json({ error: "Not authenticated" });
    if (!roles.some(role => req.user.roles.includes(role))) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }
    next();
  };
}

app.get("/admin/users", authenticate, authorize("admin"), listUsers);
```

## OAuth2 Authorization Code Flow with PKCE

```typescript
import crypto from "crypto";

function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString("base64url");
  const challenge = crypto
    .createHash("sha256")
    .update(verifier)
    .digest("base64url");
  return { verifier, challenge };
}

app.get("/auth/login", (req, res) => {
  const { verifier, challenge } = generatePKCE();
  req.session.codeVerifier = verifier;

  const params = new URLSearchParams({
    response_type: "code",
    client_id: process.env.OAUTH_CLIENT_ID!,
    redirect_uri: `${process.env.APP_URL}/auth/callb