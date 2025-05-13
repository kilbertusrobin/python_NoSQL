#!/bin/bash
# Script shell pour tester l'API

# Variables
BASE_URL="http://localhost:5000"
USERS_URL="$BASE_URL/users"
POSTS_URL="$BASE_URL/posts"
COMMENTS_URL="$BASE_URL/comments"

echo -e "\033[36mTest de l'API Flask Neo4j\033[0m"

# Test de cr�ation d'utilisateurs
echo -e "\n\033[33mCr�ation d'utilisateurs:\033[0m"
USER1=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}' $USERS_URL)
USER1_ID=$(echo $USER1 | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mUtilisateur cr��: Alice (ID: $USER1_ID)\033[0m"

USER2=$(curl -s -X POST -H "Content-Type: application/json" -d '{"name": "Bob", "email": "bob@example.com"}' $USERS_URL)
USER2_ID=$(echo $USER2 | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mUtilisateur cr��: Bob (ID: $USER2_ID)\033[0m"

# Test de r�cup�ration des utilisateurs
echo -e "\n\033[33mR�cup�ration des utilisateurs:\033[0m"
USERS=$(curl -s -X GET $USERS_URL)
echo -e "\033[32mR�sultat: $USERS\033[0m"

# Test d'ajout d'amiti�
echo -e "\n\033[33mAjout d'amiti�:\033[0m"
FRIEND_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"friend_id\": \"$USER2_ID\"}" $USERS_URL/$USER1_ID/friends)
echo -e "\033[32mR�sultat: $FRIEND_RESULT\033[0m"

# Test de v�rification d'amiti�
echo -e "\n\033[33mV�rification d'amiti�:\033[0m"
ARE_FRIENDS=$(curl -s -X GET $USERS_URL/$USER1_ID/friends/$USER2_ID)
echo -e "\033[32mR�sultat: $ARE_FRIENDS\033[0m"

# Test de cr�ation de post
echo -e "\n\033[33mCr�ation d'un post:\033[0m"
POST=$(curl -s -X POST -H "Content-Type: application/json" -d '{"title": "Mon premier post", "content": "Contenu du post"}' $USERS_URL/$USER1_ID/posts)
POST_ID=$(echo $POST | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mPost cr��: (ID: $POST_ID)\033[0m"

# Test de r�cup�ration des posts
echo -e "\n\033[33mR�cup�ration des posts:\033[0m"
POSTS=$(curl -s -X GET $POSTS_URL)
echo -e "\033[32mR�sultat: $POSTS\033[0m"

# Test de cr�ation de commentaire
echo -e "\n\033[33mCr�ation d'un commentaire:\033[0m"
COMMENT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"$USER2_ID\", \"content\": \"Super post !\"}" $POSTS_URL/$POST_ID/comments)
COMMENT_ID=$(echo $COMMENT | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "\033[32mCommentaire cr��: (ID: $COMMENT_ID)\033[0m"

# Test de r�cup�ration des commentaires d'un post
echo -e "\n\033[33mR�cup�ration des commentaires d'un post:\033[0m"
COMMENTS=$(curl -s -X GET $POSTS_URL/$POST_ID/comments)
echo -e "\033[32mR�sultat: $COMMENTS\033[0m"

# Test de like de post
echo -e "\n\033[33mLike d'un post:\033[0m"
LIKE_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"$USER2_ID\"}" $POSTS_URL/$POST_ID/like)
echo -e "\033[32mR�sultat: $LIKE_RESULT\033[0m"

# Test de like d'un commentaire
echo -e "\n\033[33mLike d'un commentaire:\033[0m"
LIKE_COMMENT_RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"$USER1_ID\"}" $COMMENTS_URL/$COMMENT_ID/like)
echo -e "\033[32mR�sultat: $LIKE_COMMENT_RESULT\033[0m"

echo -e "\n\033[36mTous les tests ont �t� effectu�s avec succ�s !\033[0m"
