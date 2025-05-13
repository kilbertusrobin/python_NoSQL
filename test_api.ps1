# Script PowerShell pour tester l'API

# Variables
$BASE_URL = "http://localhost:5000"
$USERS_URL = "$BASE_URL/users"
$POSTS_URL = "$BASE_URL/posts"
$COMMENTS_URL = "$BASE_URL/comments"

Write-Host "Test de l'API Flask Neo4j" -ForegroundColor Cyan

# Test de cr�ation d'utilisateurs
Write-Host "`nCr�ation d'utilisateurs:" -ForegroundColor Yellow
$user1 = Invoke-RestMethod -Uri $USERS_URL -Method Post -ContentType "application/json" -Body '{"name": "Alice", "email": "alice@example.com"}'
Write-Host "Utilisateur cr��: $($user1.name) (ID: $($user1.id))" -ForegroundColor Green

$user2 = Invoke-RestMethod -Uri $USERS_URL -Method Post -ContentType "application/json" -Body '{"name": "Bob", "email": "bob@example.com"}'
Write-Host "Utilisateur cr��: $($user2.name) (ID: $($user2.id))" -ForegroundColor Green

# Test de r�cup�ration des utilisateurs
Write-Host "`nR�cup�ration des utilisateurs:" -ForegroundColor Yellow
$users = Invoke-RestMethod -Uri $USERS_URL -Method Get
Write-Host "Nombre d'utilisateurs: $($users.Count)" -ForegroundColor Green
foreach ($user in $users) {
    Write-Host "- $($user.name) (ID: $($user.id))" -ForegroundColor Green
}

# Test d'ajout d'amiti�
Write-Host "`nAjout d'amiti�:" -ForegroundColor Yellow
$friendResult = Invoke-RestMethod -Uri "$USERS_URL/$($user1.id)/friends" -Method Post -ContentType "application/json" -Body "{`"friend_id`": `"$($user2.id)`"}"
Write-Host "R�sultat: $($friendResult.message)" -ForegroundColor Green

# Test de v�rification d'amiti�
Write-Host "`nV�rification d'amiti�:" -ForegroundColor Yellow
$areFriends = Invoke-RestMethod -Uri "$USERS_URL/$($user1.id)/friends/$($user2.id)" -Method Get
Write-Host "Sont-ils amis? $($areFriends.are_friends)" -ForegroundColor Green

# Test de cr�ation de post
Write-Host "`nCr�ation d'un post:" -ForegroundColor Yellow
$post = Invoke-RestMethod -Uri "$USERS_URL/$($user1.id)/posts" -Method Post -ContentType "application/json" -Body '{"title": "Mon premier post", "content": "Contenu du post"}'
Write-Host "Post cr��: $($post.title) (ID: $($post.id))" -ForegroundColor Green

# Test de r�cup�ration des posts
Write-Host "`nR�cup�ration des posts:" -ForegroundColor Yellow
$posts = Invoke-RestMethod -Uri $POSTS_URL -Method Get
Write-Host "Nombre de posts: $($posts.Count)" -ForegroundColor Green
foreach ($post in $posts) {
    Write-Host "- $($post.title) (ID: $($post.id))" -ForegroundColor Green
}

# Test de cr�ation de commentaire
Write-Host "`nCr�ation d'un commentaire:" -ForegroundColor Yellow
$comment = Invoke-RestMethod -Uri "$POSTS_URL/$($post.id)/comments" -Method Post -ContentType "application/json" -Body "{`"user_id`": `"$($user2.id)`", `"content`": `"Super post !`"}"
Write-Host "Commentaire cr��: $($comment.content) (ID: $($comment.id))" -ForegroundColor Green

# Test de r�cup�ration des commentaires d'un post
Write-Host "`nR�cup�ration des commentaires d'un post:" -ForegroundColor Yellow
$comments = Invoke-RestMethod -Uri "$POSTS_URL/$($post.id)/comments" -Method Get
Write-Host "Nombre de commentaires: $($comments.Count)" -ForegroundColor Green
foreach ($comment in $comments) {
    Write-Host "- $($comment.content) (ID: $($comment.id))" -ForegroundColor Green
}

# Test de like de post
Write-Host "`nLike d'un post:" -ForegroundColor Yellow
$likeResult = Invoke-RestMethod -Uri "$POSTS_URL/$($post.id)/like" -Method Post -ContentType "application/json" -Body "{`"user_id`": `"$($user2.id)`"}"
Write-Host "R�sultat: $($likeResult.message)" -ForegroundColor Green

# Test de like d'un commentaire
Write-Host "`nLike d'un commentaire:" -ForegroundColor Yellow
$likeCommentResult = Invoke-RestMethod -Uri "$COMMENTS_URL/$($comment.id)/like" -Method Post -ContentType "application/json" -Body "{`"user_id`": `"$($user1.id)`"}"
Write-Host "R�sultat: $($likeCommentResult.message)" -ForegroundColor Green

Write-Host "`nTous les tests ont �t� effectu�s avec succ�s !" -ForegroundColor Cyan
