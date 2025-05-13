# Script PowerShell pour tester l'API

# Variables
$BASE_URL = "http://localhost:5000"
$USERS_URL = "$BASE_URL/users"
$POSTS_URL = "$BASE_URL/posts"
$COMMENTS_URL = "$BASE_URL/comments"

Write-Host "Test de l'API Flask Neo4j" -ForegroundColor Cyan

# Test de création d'utilisateurs
Write-Host "`nCréation d'utilisateurs:" -ForegroundColor Yellow
$user1 = Invoke-RestMethod -Uri $USERS_URL -Method Post -ContentType "application/json" -Body '{"name": "Alice", "email": "alice@example.com"}'
Write-Host "Utilisateur créé: $($user1.name) (ID: $($user1.id))" -ForegroundColor Green

$user2 = Invoke-RestMethod -Uri $USERS_URL -Method Post -ContentType "application/json" -Body '{"name": "Bob", "email": "bob@example.com"}'
Write-Host "Utilisateur créé: $($user2.name) (ID: $($user2.id))" -ForegroundColor Green

# Test de récupération des utilisateurs
Write-Host "`nRécupération des utilisateurs:" -ForegroundColor Yellow
$users = Invoke-RestMethod -Uri $USERS_URL -Method Get
Write-Host "Nombre d'utilisateurs: $($users.Count)" -ForegroundColor Green
foreach ($user in $users) {
    Write-Host "- $($user.name) (ID: $($user.id))" -ForegroundColor Green
}

# Test d'ajout d'amitié
Write-Host "`nAjout d'amitié:" -ForegroundColor Yellow
$friendResult = Invoke-RestMethod -Uri "$USERS_URL/$($user1.id)/friends" -Method Post -ContentType "application/json" -Body "{`"friend_id`": `"$($user2.id)`"}"
Write-Host "Résultat: $($friendResult.message)" -ForegroundColor Green

# Test de vérification d'amitié
Write-Host "`nVérification d'amitié:" -ForegroundColor Yellow
$areFriends = Invoke-RestMethod -Uri "$USERS_URL/$($user1.id)/friends/$($user2.id)" -Method Get
Write-Host "Sont-ils amis? $($areFriends.are_friends)" -ForegroundColor Green

# Test de création de post
Write-Host "`nCréation d'un post:" -ForegroundColor Yellow
$post = Invoke-RestMethod -Uri "$USERS_URL/$($user1.id)/posts" -Method Post -ContentType "application/json" -Body '{"title": "Mon premier post", "content": "Contenu du post"}'
Write-Host "Post créé: $($post.title) (ID: $($post.id))" -ForegroundColor Green

# Test de récupération des posts
Write-Host "`nRécupération des posts:" -ForegroundColor Yellow
$posts = Invoke-RestMethod -Uri $POSTS_URL -Method Get
Write-Host "Nombre de posts: $($posts.Count)" -ForegroundColor Green
foreach ($post in $posts) {
    Write-Host "- $($post.title) (ID: $($post.id))" -ForegroundColor Green
}

# Test de création de commentaire
Write-Host "`nCréation d'un commentaire:" -ForegroundColor Yellow
$comment = Invoke-RestMethod -Uri "$POSTS_URL/$($post.id)/comments" -Method Post -ContentType "application/json" -Body "{`"user_id`": `"$($user2.id)`", `"content`": `"Super post !`"}"
Write-Host "Commentaire créé: $($comment.content) (ID: $($comment.id))" -ForegroundColor Green

# Test de récupération des commentaires d'un post
Write-Host "`nRécupération des commentaires d'un post:" -ForegroundColor Yellow
$comments = Invoke-RestMethod -Uri "$POSTS_URL/$($post.id)/comments" -Method Get
Write-Host "Nombre de commentaires: $($comments.Count)" -ForegroundColor Green
foreach ($comment in $comments) {
    Write-Host "- $($comment.content) (ID: $($comment.id))" -ForegroundColor Green
}

# Test de like de post
Write-Host "`nLike d'un post:" -ForegroundColor Yellow
$likeResult = Invoke-RestMethod -Uri "$POSTS_URL/$($post.id)/like" -Method Post -ContentType "application/json" -Body "{`"user_id`": `"$($user2.id)`"}"
Write-Host "Résultat: $($likeResult.message)" -ForegroundColor Green

# Test de like d'un commentaire
Write-Host "`nLike d'un commentaire:" -ForegroundColor Yellow
$likeCommentResult = Invoke-RestMethod -Uri "$COMMENTS_URL/$($comment.id)/like" -Method Post -ContentType "application/json" -Body "{`"user_id`": `"$($user1.id)`"}"
Write-Host "Résultat: $($likeCommentResult.message)" -ForegroundColor Green

Write-Host "`nTous les tests ont été effectués avec succès !" -ForegroundColor Cyan
