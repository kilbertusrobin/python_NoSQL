#!/bin/bash
# Script shell pour tester l'API

# Variables
BASE_URL="http://localhost:5000"
USERS_URL="$BASE_URL/users"
POSTS_URL="$BASE_URL/posts"
COMMENTS_URL="$BASE_URL/comments"

echo -e "\033[36mTest de l'API Flask Neo4j\033[0m"

# Test de création d'utilisateurs
echo -e "\n\033[33mCréation d'utilisateurs:\033[0m"
USER1=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}' $USERS_URL)
USER1_ID=$(echo $USER1 | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mUtilisateur créé: Alice (ID: $USER1_ID)\033[0m"

USER2=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "Bob", "email": "bob@example.com"}' $USERS_URL)
USER2_ID=$(echo $USER2 | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mUtilisateur créé: Bob (ID: $USER2_ID)\033[0m"

# Test de récupération des utilisateurs
echo -e "\n\033[33mRécupération des utilisateurs:\033[0m"
USERS=$(curl -s -X GET $USERS_URL)
echo -e "\033[32mRésultat: $USERS\033[0m"

# Test d'ajout d'amitié
echo -e "\n\033[33mAjout d'amitié:\033[0m"
FRIEND_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"friend_id\": \"$USER2_ID\"}" $USERS_URL/$USER1_ID/friends)
echo -e "\033[32mRésultat: $FRIEND_RESULT\033[0m"

# Test de vérification d'amitié
echo -e "\n\033[33mVérification d'amitié:\033[0m"
ARE_FRIENDS=$(curl -s -X GET $USERS_URL/$USER1_ID/friends/$USER2_ID)
echo -e "\033[32mRésultat: $ARE_FRIENDS\033[0m"

# Test de création de post
echo -e "\n\033[33mCréation d'un post:\033[0m"
POST=$(curl -s -X POST -H "Content-Type: application/json" -d '{"title": "Mon premier post", "content": "Contenu du post"}' $USERS_URL/$USER1_ID/posts)
POST_ID=$(echo $POST | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mPost créé: (ID: $POST_ID)\033[0m"

# Test de récupération des posts
echo -e "\n\033[33mRécupération des posts:\033[0m"
POSTS=$(curl -s -X GET $POSTS_URL)
echo -e "\033[32mRésultat: $POSTS\033[0m"

# Test de création de commentaire
echo -e "\n\033[33mCréation d'un commentaire:\033[0m"
COMMENT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"$USER2_ID\", \"content\": \"Super post !\"}" $POSTS_URL/$POST_ID/comments)
COMMENT_ID=$(echo $COMMENT | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mCommentaire créé: (ID: $COMMENT_ID)\033[0m"

# Test de récupération des commentaires d'un post
echo -e "\n\033[33mRécupération des commentaires d'un post:\033[0m"
COMMENTS=$(curl -s -X GET $POSTS_URL/$POST_ID/comments)
echo -e "\033[32mRésultat: $COMMENTS\033[0m"

# Test de like de post
echo -e "\n\033[33mLike d'un post:\033[0m"
LIKE_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"$USER2_ID\"}" $POSTS_URL/$POST_ID/like)
echo -e "\033[32mRésultat: $LIKE_RESULT\033[0m"

# Test de like d'un commentaire
echo -e "\n\033[33mLike d'un commentaire:\033[0m"
LIKE_COMMENT_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"$USER1_ID\"}" $COMMENTS_URL/$COMMENT_ID/like)
echo -e "\033[32mRésultat: $LIKE_COMMENT_RESULT\033[0m"

echo -e "\n\033[36mTous les tests ont été effectués avec succès !\033[0m"
